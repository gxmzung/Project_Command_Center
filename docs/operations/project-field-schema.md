# Project Command Center Field Schema

GitHub Projects에 추가할 필드 표준안이다.

## 필수 필드

| Field | Type | Example | Purpose |
|---|---|---|---|
| Project | Select | CityBrain / SkyEdge / BioDockLab / UAM Radio Ops | 상위 프로젝트 |
| Sub Project | Text | Android App / Backend API / Admin Web / Docs | 세부 작업 묶음 |
| Department | Select | 컴퓨터공학 / AI / 게임공학 / 생명공학 / 항공드론 / 경영 | 참여자 전공 |
| Role | Select | PM / Backend / Frontend / Mobile / Data / DevOps / HW / SW / Docs | 실제 역할 |
| Skill Track | Text | FastAPI, Kotlin, ROS2, PX4, GitHub Ops | 공부/훈련 방향 |
| Assignee | Person | @nickname | 담당자 |
| Status | Select | Inbox / Todo / In Progress / Review / Blocked / Done / Archived | 진행 상태 |
| Priority | Select | P0 / P1 / P2 / P3 | 우선순위 |
| Start Date | Date | 2026-05-20 | 착수일 |
| Target Date | Date | 2026-05-30 | 목표일 |
| Progress % | Number | 0 / 25 / 50 / 75 / 100 | 진행률 |
| Related Repository | Text | gxmzung/CityBrain | 관련 레포 |
| Related Issue | Text | #12 | 관련 이슈 |
| Evidence / Output | Text | docs/test-logs, screenshots, demo video | 증거자료 |
| Blocker | Text | API 미완성, 자료 부족, 팀원 미응답 | 막힌 이유 |
| Next Action | Text | API 명세 확정, 화면 캡처, 테스트 로그 추가 | 다음 행동 |

## Status 기준

### Inbox
아직 분류되지 않은 아이디어나 요청.

### Todo
실행하기로 결정했지만 아직 시작하지 않은 작업.

### In Progress
실제로 코드, 문서, 조사, 디자인 작업이 진행 중인 상태.

### Review
검토, 피드백, 발표자료 반영, 코드리뷰가 필요한 상태.

### Blocked
외부 자료, 팀원 응답, API 키, 장비, 교수 피드백 등으로 막힌 상태.

### Done
산출물이 존재하고 검토 가능한 상태.

### Archived
현재는 보류하거나 종료한 작업.

## Progress % 기준

| Progress | 기준 |
|---|---|
| 0% | 아이디어만 있음 |
| 25% | 작업 범위와 담당자가 정해짐 |
| 50% | 초안/프로토타입/기본 코드가 있음 |
| 75% | 검토 가능한 산출물이 있음 |
| 100% | 제출/시연/병합/문서화 완료 |

주의: Progress %는 기분으로 올리지 않는다. 산출물이 있어야 올라간다.
