#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


OWNER = "gxmzung"
PROJECT_NUMBER = "5"


def run(cmd, check=True):
    print("+", " ".join(cmd))
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result


def load_issue(path):
    data = json.loads(Path(path).read_text())
    return {
        "number": str(data.get("number", "")),
        "title": data.get("title") or "",
        "body": data.get("body") or "",
        "url": data.get("url") or data.get("htmlUrl") or "",
    }


def parse_issue_form(body):
    """
    GitHub Issue Form markdown 예시:

    ### Project

    Project_Command_Center

    ### Role

    DevOps / GitHub Ops
    """
    sections = {}
    pattern = re.compile(r"^###\s+(.+?)\s*\n+(.*?)(?=\n###\s+|\Z)", re.M | re.S)

    for match in pattern.finditer(body or ""):
        key = match.group(1).strip()
        value = match.group(2).strip()

        value = re.sub(r"<!--.*?-->", "", value, flags=re.S).strip()
        if value in {"_No response_", "No response", "없음", "-"}:
            value = ""

        sections[key] = value

    return sections


def normalize(value):
    return re.sub(r"\s+", " ", (value or "").strip()).lower()


def get_project_id():
    result = run(
        ["gh", "project", "view", PROJECT_NUMBER, "--owner", OWNER, "--format", "json"],
        check=True,
    )
    return json.loads(result.stdout)["id"]


def get_fields():
    result = run(
        ["gh", "project", "field-list", PROJECT_NUMBER, "--owner", OWNER, "--format", "json", "-L", "100"],
        check=True,
    )
    return json.loads(result.stdout).get("fields", [])


def find_field(fields, name):
    for field in fields:
        if field.get("name") == name:
            return field
    return None


def find_option(field, raw_value):
    if not field or not raw_value:
        return None

    value = normalize(raw_value)
    options = field.get("options") or []

    # 1. exact
    for option in options:
        if normalize(option.get("name")) == value:
            return option

    # 2. partial: "컴퓨터공학과" -> "컴퓨터공학"
    for option in options:
        opt = normalize(option.get("name"))
        if opt and (opt in value or value in opt):
            return option

    # 3. priority shorthand: P1 -> P1 - High
    for option in options:
        opt = normalize(option.get("name"))
        if value and opt.startswith(value):
            return option

    return None


def ensure_project_item(issue):
    url = issue["url"]
    if not url:
        raise SystemExit("Issue URL not found")

    # 먼저 추가 시도. 이미 들어가 있으면 실패할 수 있으므로 fallback으로 item-list 검색.
    result = run(
        ["gh", "project", "item-add", PROJECT_NUMBER, "--owner", OWNER, "--url", url, "--format", "json"],
        check=False,
    )

    if result.returncode == 0 and result.stdout.strip():
        try:
            data = json.loads(result.stdout)
            if data.get("id"):
                return data["id"]
        except json.JSONDecodeError:
            pass

    print("item-add failed or already exists. Searching existing project items...")

    result = run(
        ["gh", "project", "item-list", PROJECT_NUMBER, "--owner", OWNER, "--format", "json", "-L", "500"],
        check=True,
    )
    items = json.loads(result.stdout).get("items", [])

    for item in items:
        content = item.get("content") or {}
        if content.get("url") == url:
            return item["id"]
        if str(content.get("number", "")) == issue["number"] and content.get("title") == issue["title"]:
            return item["id"]
        if content.get("title") == issue["title"]:
            return item["id"]

    raise SystemExit("Project item not found after add/search")


def edit_text(project_id, item_id, field, value):
    if not field or not value:
        return
    run([
        "gh", "project", "item-edit",
        "--id", item_id,
        "--project-id", project_id,
        "--field-id", field["id"],
        "--text", value,
    ])


def edit_number(project_id, item_id, field, value):
    if not field or value is None or value == "":
        return

    match = re.search(r"\d+(\.\d+)?", str(value))
    if not match:
        return

    number = float(match.group(0))

    # gh CLI 일부 버전에서 --number 0 처리가 애매할 수 있어 0은 생략한다.
    if number <= 0:
        return

    run([
        "gh", "project", "item-edit",
        "--id", item_id,
        "--project-id", project_id,
        "--field-id", field["id"],
        "--number", str(number),
    ])


def edit_date(project_id, item_id, field, value):
    if not field or not value:
        return

    match = re.search(r"\d{4}-\d{2}-\d{2}", value)
    if not match:
        return

    run([
        "gh", "project", "item-edit",
        "--id", item_id,
        "--project-id", project_id,
        "--field-id", field["id"],
        "--date", match.group(0),
    ])


def edit_select(project_id, item_id, field, value):
    if not field or not value:
        return

    option = find_option(field, value)
    if not option:
        print(f"SKIP select field '{field.get('name')}' because option not found for value: {value}")
        return

    run([
        "gh", "project", "item-edit",
        "--id", item_id,
        "--project-id", project_id,
        "--field-id", field["id"],
        "--single-select-option-id", option["id"],
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-json", required=True)
    args = parser.parse_args()

    issue = load_issue(args.issue_json)
    sections = parse_issue_form(issue["body"])

    print("Parsed issue form sections:")
    print(json.dumps(sections, ensure_ascii=False, indent=2))

    project_id = get_project_id()
    fields = get_fields()
    item_id = ensure_project_item(issue)

    field = lambda name: find_field(fields, name)

    values = {
        "Project": sections.get("Project") or "Project_Command_Center",
        "Sub Project": sections.get("Sub Project"),
        "Department": sections.get("Department / Major") or sections.get("Department"),
        "Role": sections.get("Role"),
        "Skill Track": sections.get("Skill Track"),
        "Priority": sections.get("Priority") or "P2 - Normal",
        "Target Date": sections.get("Target Date"),
        "Progress %": sections.get("Progress %"),
        "Evidence / Output": sections.get("Evidence / Output"),
        "Blocker": sections.get("Blocker"),
        "Next Action": sections.get("Next Action"),
        "Related Repository": os.environ.get("GITHUB_REPOSITORY", "gxmzung/Project_Command_Center"),
        "Related Issue": f"#{issue['number']}" if issue["number"] else "",
    }

    edit_select(project_id, item_id, field("Project"), values["Project"])
    edit_text(project_id, item_id, field("Sub Project"), values["Sub Project"])
    edit_select(project_id, item_id, field("Department"), values["Department"])
    edit_select(project_id, item_id, field("Role"), values["Role"])
    edit_text(project_id, item_id, field("Skill Track"), values["Skill Track"])
    edit_select(project_id, item_id, field("Priority"), values["Priority"])
    edit_date(project_id, item_id, field("Target Date"), values["Target Date"])
    edit_number(project_id, item_id, field("Progress %"), values["Progress %"])
    edit_text(project_id, item_id, field("Related Repository"), values["Related Repository"])
    edit_text(project_id, item_id, field("Related Issue"), values["Related Issue"])
    edit_text(project_id, item_id, field("Evidence / Output"), values["Evidence / Output"])
    edit_text(project_id, item_id, field("Blocker"), values["Blocker"])
    edit_text(project_id, item_id, field("Next Action"), values["Next Action"])

    # 기본 Status 필드가 있으면 Todo로 자동 세팅
    status_field = field("Status")
    if status_field:
        edit_select(project_id, item_id, status_field, "Todo")

    print("DONE: Project fields synced.")


if __name__ == "__main__":
    main()
