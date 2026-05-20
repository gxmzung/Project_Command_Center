# Reference Repository Absorption Notes

이 문서는 외부 참고 레포의 구조를 Project Command Center에 흡수하기 위한 기준 문서다.

## 1. github/roadmap에서 흡수할 것

### 핵심
공개 로드맵은 단순 TODO가 아니라, 큰 목표를 이슈/프로젝트 단위로 쪼개서 관리한다.

### 흡수 방식
- Project / Sub Project 필드로 큰 단위를 나눈다.
- Issue는 실행 가능한 최소 작업 단위로 만든다.
- Status, Priority, Target Date, Progress를 필수 필드로 둔다.
- 로드맵은 README가 아니라 GitHub Projects가 원본이 되게 한다.

## 2. actions/add-to-project에서 흡수할 것

### 핵심
새 Issue/PR이 생기면 자동으로 GitHub Project에 들어가게 만든다.

### 흡수 방식
- 모든 작업은 Issue로 등록한다.
- Issue가 열리면 자동으로 Project Command Center 보드에 추가한다.
- 수동 누락을 줄여서 프로젝트 관리판을 실제 운영 DB처럼 쓴다.

## 3. issue-metrics에서 흡수할 것

### 핵심
이슈 처리 속도, 첫 응답 시간, 완료 시간 같은 운영 지표를 자동 보고서로 만든다.

### 흡수 방식
- 매월 Issue Metrics Report를 자동 생성한다.
- 단순 커밋 수가 아니라 작업 처리 흐름을 본다.
- 팀원이 많아질수록 “누가 열심히 했는가”보다 “어디서 막혔는가”를 본다.

## 4. upptime에서 흡수할 것

### 핵심
GitHub 자체를 운영 상태판으로 쓴다.

### 흡수 방식
- 프로젝트별 상태를 Green / Yellow / Red로 표시한다.
- 장애, 지연, 리스크는 숨기지 않고 기록한다.
- 프로젝트 신뢰도는 결과물보다 운영 로그에서 나온다.

## 5. backstage에서 흡수할 것

### 핵심
여러 서비스/레포/문서를 한눈에 보는 개발자 포털 구조.

### 흡수 방식
- Related Repository 필드를 둔다.
- 각 프로젝트마다 README, Runbook, Evidence, Meeting Notes 링크를 연결한다.
- 사람 중심이 아니라 시스템/서비스 중심으로 관리한다.

## 6. Worklenz류 PM 도구에서 흡수할 것

### 핵심
작업, 일정, 담당자, 우선순위, 진행률을 구조화한다.

### 흡수 방식
- Master Schedule을 별도 문서화한다.
- Progress %는 감으로 적지 않고 산출물 기준으로 계산한다.
- 역할은 “개발자” 한 줄이 아니라 학과/직무/스킬트랙까지 분해한다.

## 결론

Project Command Center는 예쁜 README 레포가 아니라 다음 역할을 해야 한다.

1. 프로젝트 전체 상황판
2. 팀원 역할/학습 방향 관리판
3. GitHub Issue 기반 실행 관리판
4. 발표/대회/포트폴리오 증거 보관소
5. 장기적으로는 여러 레포를 묶는 운영 OS
