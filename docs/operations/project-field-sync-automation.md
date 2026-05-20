# Project Field Sync Automation

이 자동화는 GitHub Issue Form에 입력된 값을 Project Command Center의 GitHub Project 필드로 동기화한다.

## Workflow

- `.github/workflows/sync-project-fields.yml`

## Script

- `scripts/sync_project_fields.py`

## Trigger

다음 상황에서 실행된다.

- Issue opened
- Issue edited
- Issue reopened
- Manual workflow_dispatch

## Required Secret

- `ADD_TO_PROJECT_PAT`

필요 권한:

- Repository Issues read
- Repository Pull Requests read
- Project read/write

## Synced Fields

| Issue Form Section | Project Field |
|---|---|
| Project | Project |
| Sub Project | Sub Project |
| Department / Major | Department |
| Role | Role |
| Skill Track | Skill Track |
| Priority | Priority |
| Target Date | Target Date |
| Progress % | Progress % |
| Evidence / Output | Evidence / Output |
| Blocker | Blocker |
| Next Action | Next Action |

자동으로 들어가는 값:

| Value | Rule |
|---|---|
| Related Repository | 현재 GitHub repository |
| Related Issue | 현재 issue number |
| Status | Todo, 필드와 옵션이 존재할 때만 |

## 운영 규칙

1. 작업은 반드시 Issue로 만든다.
2. Issue Form의 항목명을 함부로 바꾸지 않는다.
3. Project 필드 옵션명을 바꾸면 sync script도 같이 확인한다.
4. Progress %는 산출물이 있을 때만 올린다.
5. workflow_dispatch로 기존 이슈도 다시 동기화할 수 있다.

## Known Limits

- Project single select option에 없는 값은 자동 입력되지 않는다.
- Progress %가 0이면 일부 gh CLI 버전에서 의미 없는 변경으로 처리될 수 있어 생략한다.
- Issue body가 표준 Issue Form 형식이 아니면 일부 필드는 비어 있을 수 있다.
