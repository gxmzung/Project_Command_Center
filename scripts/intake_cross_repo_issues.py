#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


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


def normalize(value):
    return re.sub(r"\s+", " ", str(value or "").strip()).lower()


def gh_json(cmd, fallback=None, check=True):
    result = run(cmd, check=check)
    if result.returncode != 0:
        return fallback
    if not result.stdout.strip():
        return fallback
    return json.loads(result.stdout)


def find_field(fields, name):
    for field in fields:
        if field.get("name") == name:
            return field
    return None


def find_option(field, value):
    if not field or not value:
        return None

    target = normalize(value)

    for option in field.get("options") or []:
        if normalize(option.get("name")) == target:
            return option

    for option in field.get("options") or []:
        opt = normalize(option.get("name"))
        if opt and (opt in target or target in opt):
            return option

    for option in field.get("options") or []:
        opt = normalize(option.get("name"))
        if target and opt.startswith(target):
            return option

    return None


def edit_text(project_id, item_id, field, value, dry_run=False):
    if not field or not value:
        return

    cmd = [
        "gh", "project", "item-edit",
        "--id", item_id,
        "--project-id", project_id,
        "--field-id", field["id"],
        "--text", str(value),
    ]

    if dry_run:
        print("[DRY RUN]", " ".join(cmd))
    else:
        run(cmd)


def edit_select(project_id, item_id, field, value, dry_run=False):
    if not field or not value:
        return

    option = find_option(field, value)
    if not option:
        print(f"SKIP select field {field.get('name')} because option not found: {value}")
        return

    cmd = [
        "gh", "project", "item-edit",
        "--id", item_id,
        "--project-id", project_id,
        "--field-id", field["id"],
        "--single-select-option-id", option["id"],
    ]

    if dry_run:
        print("[DRY RUN]", " ".join(cmd))
    else:
        run(cmd)


def label_names(issue):
    return [label.get("name", "") for label in issue.get("labels") or []]


def infer_priority(labels):
    lowered = [normalize(x) for x in labels]

    if any(x in lowered for x in ["p0", "critical", "urgent", "긴급"]):
        return "P0 - Critical"
    if any(x in lowered for x in ["p1", "high", "important", "중요"]):
        return "P1 - High"
    if any(x in lowered for x in ["p3", "low", "minor"]):
        return "P3 - Low"

    return "P2 - Normal"


def infer_role(labels, default_role):
    lowered = [normalize(x) for x in labels]

    role_map = [
        ("backend", "Backend"),
        ("api", "Backend"),
        ("server", "Backend"),
        ("frontend", "Frontend"),
        ("web", "Frontend"),
        ("mobile", "Mobile"),
        ("android", "Mobile"),
        ("data", "Data"),
        ("analytics", "Data"),
        ("devops", "DevOps / GitHub Ops"),
        ("github", "DevOps / GitHub Ops"),
        ("automation", "DevOps / GitHub Ops"),
        ("hardware", "Hardware / Embedded"),
        ("embedded", "Hardware / Embedded"),
        ("firmware", "Hardware / Embedded"),
        ("docs", "Research / Documentation"),
        ("documentation", "Research / Documentation"),
        ("research", "Research / Documentation"),
        ("design", "Design / UX"),
        ("ux", "Design / UX"),
        ("business", "Business / Operations"),
        ("ops", "Business / Operations")
    ]

    for key, role in role_map:
        if key in lowered:
            return role

    for label in lowered:
        for key, role in role_map:
            if key in label:
                return role

    return default_role


def infer_status(labels):
    lowered = [normalize(x) for x in labels]

    if any(x in lowered for x in ["blocked", "blocker", "막힘"]):
        return "Blocked"
    if any(x in lowered for x in ["in progress", "doing", "wip"]):
        return "In Progress"
    if any(x in lowered for x in ["review", "needs-review"]):
        return "Review"
    if any(x in lowered for x in ["done", "complete", "completed"]):
        return "Done"

    return "Todo"


def get_project_id(owner, project_number):
    data = gh_json([
        "gh", "project", "view", str(project_number),
        "--owner", owner,
        "--format", "json"
    ])
    return data["id"]


def get_fields(owner, project_number):
    data = gh_json([
        "gh", "project", "field-list", str(project_number),
        "--owner", owner,
        "--format", "json",
        "-L", "100"
    ])
    return data.get("fields", [])


def get_existing_items(owner, project_number):
    data = gh_json([
        "gh", "project", "item-list", str(project_number),
        "--owner", owner,
        "--format", "json",
        "-L", "1000"
    ], fallback={"items": []})
    return data.get("items", [])


def find_existing_item_id(items, issue_url):
    for item in items:
        content = item.get("content") or {}
        if content.get("url") == issue_url:
            return item.get("id")
    return None


def add_or_get_item(owner, project_number, issue_url, existing_items, dry_run=False):
    existing = find_existing_item_id(existing_items, issue_url)
    if existing:
        print(f"EXISTS in project: {issue_url}")
        return existing

    if dry_run:
        print(f"[DRY RUN] gh project item-add {project_number} --owner {owner} --url {issue_url}")
        return "DRY_RUN_ITEM_ID"

    data = gh_json([
        "gh", "project", "item-add", str(project_number),
        "--owner", owner,
        "--url", issue_url,
        "--format", "json"
    ], fallback=None, check=False)

    if data and data.get("id"):
        return data["id"]

    refreshed = get_existing_items(owner, project_number)
    existing = find_existing_item_id(refreshed, issue_url)
    if existing:
        return existing

    raise SystemExit(f"Failed to add/find project item: {issue_url}")


def list_open_issues(repo, limit):
    data = gh_json([
        "gh", "issue", "list",
        "--repo", repo,
        "--state", "open",
        "--limit", str(limit),
        "--json", "number,title,url,labels,assignees,state,createdAt,updatedAt"
    ], fallback=None, check=False)

    if data is None:
        print(f"SKIP repo unavailable or no permission: {repo}")
        return []

    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=".github/project-command-center/repo-intake.json")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text())

    owner = config["owner"]
    project_number = config["project_number"]

    project_id = get_project_id(owner, project_number)
    fields = get_fields(owner, project_number)
    existing_items = get_existing_items(owner, project_number)

    field = lambda name: find_field(fields, name)

    total = 0
    added_or_synced = 0

    for repo_cfg in config["repos"]:
        repo = repo_cfg["repo"]
        print("")
        print("=" * 80)
        print(f"REPO: {repo}")
        print("=" * 80)

        issues = list_open_issues(repo, args.limit)
        total += len(issues)

        for issue in issues:
            labels = label_names(issue)

            issue_url = issue["url"]
            item_id = add_or_get_item(
                owner=owner,
                project_number=project_number,
                issue_url=issue_url,
                existing_items=existing_items,
                dry_run=args.dry_run
            )

            project_value = repo_cfg.get("project", "Other")
            sub_project = repo_cfg.get("sub_project", repo)
            role = infer_role(labels, repo_cfg.get("default_role", "Other"))
            priority = infer_priority(labels)
            status = infer_status(labels)
            skill_track = repo_cfg.get("skill_track", "")

            print(f"SYNC: #{issue['number']} {issue['title']}")
            print(f"  Project={project_value}")
            print(f"  Sub Project={sub_project}")
            print(f"  Role={role}")
            print(f"  Priority={priority}")
            print(f"  Status={status}")

            edit_select(project_id, item_id, field("Project"), project_value, args.dry_run)
            edit_text(project_id, item_id, field("Sub Project"), sub_project, args.dry_run)
            edit_select(project_id, item_id, field("Role"), role, args.dry_run)
            edit_text(project_id, item_id, field("Skill Track"), skill_track, args.dry_run)
            edit_select(project_id, item_id, field("Priority"), priority, args.dry_run)
            edit_select(project_id, item_id, field("Status"), status, args.dry_run)
            edit_text(project_id, item_id, field("Related Repository"), repo, args.dry_run)
            edit_text(project_id, item_id, field("Related Issue"), f"#{issue['number']}", args.dry_run)
            edit_text(project_id, item_id, field("Next Action"), "원본 이슈에서 작업 상태 확인 후 다음 액션 갱신", args.dry_run)

            added_or_synced += 1

    print("")
    print("=" * 80)
    print("CROSS-REPO INTAKE SUMMARY")
    print("=" * 80)
    print(f"Total open issues scanned: {total}")
    print(f"Project items added/synced: {added_or_synced}")


if __name__ == "__main__":
    main()
