# 01-B: EMR Viewer, 목표 기반 (`/goal`)

MIMIC-IV Demo 데이터로 EMR Data Viewer를 만듭니다. 환자를 찾고 그 환자의 입원·진단·처방·검사를 볼 수 있는 로컬 웹 애플리케이션입니다.

## 목차

- [이 트랙의 방식](#이-트랙의-방식)
- [`/goal` 활성화](#goal-활성화)
- [승인 정책](#승인-정책)
- [시작](#시작)
- [원본 데이터](#원본-데이터)

## 이 트랙의 방식

`/goal`은 Codex가 여러 턴에 걸쳐 하나의 목표를 계속 추구하는 기능입니다. 계획을 세우고, 구현하고, 스스로 검증하고, 실패하면 고치는 루프를 반복하다가, 성공 기준을 달성했다고 판단하면 멈춥니다.

목표를 쓰는 것이 이 트랙에서 하는 일입니다. OpenAI의 [`define-goal`](https://github.com/openai/skills/tree/main/skills/.curated/define-goal) 스킬은 쓸 수 있는 목표가 다섯 가지에 답해야 한다고 정의합니다.

- 끝났을 때 무엇이 참이 되는가
- 그것을 무엇으로 증명하는가
- 성공을 가르는 수치나 이진 기준은 무엇인가
- 어디까지가 범위인가
- 무엇을 만나면 멈추고 물어야 하는가

같은 스킬이 활동을 서술한 목표를 거부합니다. `EMR viewer 만들어줘`는 활동이고, [`goals/`](./goals/)의 세 파일은 각각 다섯 가지에 답한 목표입니다.

한 번에 앱 전체를 목표로 걸지 않고 화면 단위로 세 번 나눠 겁니다. 환자 기본 뷰, 도메인 뷰, 시간축 뷰. 앞 단계가 끝나야 다음 단계를 겁니다.

성공 기준은 전부 기계적으로 확인 가능한 것들입니다. 빌드가 되는지, 테스트가 통과하는지, 라우트가 열리는지.

## `/goal` 활성화

`/goal`은 feature flag로 게이팅되어 있습니다. 먼저 켜야 합니다.

```bash
codex features enable goals
```

그다음 Codex를 재시작하고 `/goal`이 목록에 있는지 확인하세요.

안 보이면 버전을 확인합니다.

```bash
codex --version          # 0.128.0 이상이어야 합니다
```

그래도 없으면 `~/.codex/config.toml`에 직접 추가하고 재시작합니다.

```toml
[features]
goals = true
```

## 승인 정책

`/goal`은 오래 자율 실행됩니다. 명령마다 승인을 물으면 그 자율성이 끊깁니다. 시작 전에 승인 수준을 조정하세요.

```text
/permissions
```

## 시작

```bash
cd projects/01-B-emr-viewer-goal
codex
```

`goals/`의 다음 단계를 읽히고 등록합니다. 아래는 1단계이고, 2단계와 3단계도 파일 이름만 바꿔 같은 방식으로 진행합니다.

```text
goals/README.md 와 goals/01-patient-view.md 를 읽고 그 내용을 목표로 삼아라.
```

```text
/goal goals/01-patient-view.md 의 목표와 성공 기준을 달성한다
```

돌아가는 동안 상태를 보고, 멈춰서 들여다보고, 이어서 진행합니다.

```text
/goal
/goal pause
/goal resume
```

달성했다고 보고하면 정리합니다.

```text
/goal clear
```

## 원본 데이터

- `data/mimic-iv-clinical-database-demo-2.2.zip`은 공개 배포되는 MIMIC-IV Clinical Database Demo v2.2입니다.
- 데이터 구성과 라이선스 상세는 [`goals/README.md`](./goals/)의 참고 자료에 있습니다.
- 원본 ZIP을 수정하거나 덮어쓰지 마세요.
- ODC Open Database License(ODbL)로 배포됩니다.
- 여기서 만든 것은 교육용이며 임상에 쓰지 않습니다.
