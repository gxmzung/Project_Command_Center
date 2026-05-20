# Cross-Repo Issue Intake

Project Command Center는 여러 레포의 이슈를 중앙 GitHub Project #5로 모으는 방식으로 운영한다.

## Purpose

각 프로젝트 레포에 흩어진 이슈를 하나의 중앙 보드에서 보기 위함이다.

## Source Repositories

설정 파일:

- `.github/project-command-center/repo-intake.json`

## Workflow

- `.github/workflows/cross-repo-intake.yml`

## Script

- `scripts/intake_cross_repo_issues.py`

## Behavior

각 레포의 open issue를 읽어서 Project #5에 추가한다.

자동 입력 필드:

| Field | Rule |
|---|---|
| Project | repo-intake.json의 project 값 |
| Sub Project | repo-intake.json의 sub_project 값 |
| Role | label 기반 추론, 없으면 default_role |
| Skill Track | repo-intake.json의 skill_track 값 |
| Priority | label 기반 추론, 없으면 P2 - Normal |
| Status | blocked/review/wip/done label 기반 추론, 없으면 Todo |
| Related Repository | 원본 레포 |
| Related Issue | 원본 이슈 번호 |
| Next Action | 기본 확인 문구 |

## Label Inference

### Priority

| Label | Priority |
|---|---|
| p0, critical, urgent, 긴급 | P0 - Critical |
| p1, high, important, 중요 | P1 - High |
| p3, low, minor | P3 - Low |
| none | P2 - Normal |

### Role

| Label | Role |
|---|---|
| backend, api, server | Backend |
| frontend, web | Frontend |
| mobile, android | Mobile |
| data, analytics | Data |
| devops, github, automation | DevOps / GitHub Ops |
| hardware, embedded, firmware | Hardware / Embedded |
| docs, documentation, research | Research / Documentation |
| design, ux | Design / UX |
| business, ops | Business / Operations |

## Required Secret

- `ADD_TO_PROJECT_PAT`

이 토큰은 중앙 레포뿐 아니라 intake 대상 레포의 issue 읽기 권한과 Project read/write 권한이 있어야 한다.

## Operating Rule

중앙 Project #5는 상황판이고, 실제 논의와 세부 작업은 원본 레포 이슈에서 진행한다.
