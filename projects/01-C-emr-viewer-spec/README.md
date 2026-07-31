# 01-C: EMR Viewer, 명세 기반 (spec-driven)

원본 MIMIC-IV Clinical Database Demo v2.2 ZIP에서 출발해 EMR Data Viewer를 만듭니다.

완성된 애플리케이션이 아닙니다. **페이지별 상세 요구사항도 들어 있지 않습니다.** 각 단계에서 무엇을 만들지는 여러분이 스펙으로 씁니다.

## 목차

- [이 트랙의 방식](#이-트랙의-방식)
- [포함된 파일](#포함된-파일)
- [의도적으로 넣지 않은 것](#의도적으로-넣지-않은-것)
- [시작](#시작)
- [원본 데이터](#원본-데이터)
- [참고 자료](#참고-자료)

## 이 트랙의 방식

```text
원칙과 목적을 읽는다
→ 이번 단계에서 무엇을 왜 만들지 스펙으로 쓴다
→ 모호한 곳을 되묻는다
→ 어떻게 만들지 계획한다
→ 무엇을 보면 끝난 것인지 먼저 정한다
→ 문서들이 서로 어긋나지 않는지 검사한다
→ 구현한다
→ 사람이 직접 확인한다
→ 다음 단계로
```

이것을 spec-driven development라고 합니다.

## 포함된 파일

```text
01-C-emr-viewer-spec/
├── README.md
├── prompts/
│   ├── README.md
│   └── 01 ... 09
├── specs/
│   ├── constitution.md
│   ├── mission.md
│   ├── tech-stack.md
│   └── roadmap.md
├── assets/
└── data/
    └── mimic-iv-clinical-database-demo-2.2.zip
```

- `prompts/`: 단계별 프롬프트와 사람이 확인할 것
- `specs/constitution.md`: 모든 단계에 적용되는 절대 규칙 9개. 스펙보다 우선합니다
- `specs/mission.md`: 왜 만드는가, 누구를 위한 것인가, 성공이란, 비목표
- `specs/tech-stack.md`: 고정된 기술 스택과 쓰지 않는 것
- `specs/roadmap.md`: 세 단계 목록. 단계별 목표 한 줄과 반드시 지킬 원칙
- `assets/`: 정적 자산을 두는 곳. 지금은 비어 있습니다
- `data/...zip`: 수정하지 않은 원본 Demo 데이터

여러분이 만들 문서는 단계마다 `specs/<번호>-<단계이름>/` 아래에 생깁니다.

```text
specs/001-patient-view/
├── spec.md        무엇을, 왜 (기술 선택 없이)
├── plan.md        어떻게 (기술 선택 포함)
├── tasks.md       어떤 순서로
└── checklist.md   무엇을 보면 끝난 것인가
```

## 의도적으로 넣지 않은 것

- 페이지별 상세 요구사항. 이것이 여러분이 `spec.md`에 쓸 내용입니다
- React/Vite 프로젝트나 애플리케이션 코드
- 압축을 푼 CSV, 데이터베이스, 파생 JSON, 전처리 스크립트
- 완성된 참조 구현이나 모범 답안

## 시작

```bash
cd projects/01-C-emr-viewer-spec
```

**[`prompts/`](./prompts/)의 01번 파일부터 순서대로 진행하세요.** 한 번에 한 파일만 봅니다.

## 원본 데이터

- `data/mimic-iv-clinical-database-demo-2.2.zip`은 공개 배포되는 MIMIC-IV Clinical Database Demo v2.2입니다.
- Beth Israel Deaconess Medical Center의 비식별화된 EHR 데이터 기반이고, 환자 100명 부분집합입니다.
- 임상 테이블 31개가 들어 있습니다. `hosp` 22개, `icu` 9개.
- 자유 서술형 임상 노트는 포함되지 않습니다.
- ZIP 안에 `README.txt`, `LICENSE.txt`, `SHA256SUMS.txt`가 있습니다.
- ZIP의 SHA-256은 `97301a03820e8f41af211cf3462ddc19aefe75bbed05f11753859affaafeb8ec`이고, 실습 전후로 같아야 합니다.
- 원본 ZIP을 수정하거나 덮어쓰지 마세요. 압축을 풀거나 변환한 결과는 별도 경로에 만드세요.
- ODC Open Database License(ODbL)로 배포됩니다. 데이터셋 상세는 <https://doi.org/10.13026/07hj-2a80>.
- 여기서 만든 것은 교육용이며 임상에 쓰지 않습니다.

## 참고 자료

단계 이름(`specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`)과 artifact 구성은 GitHub의 Spec Kit에서 가져왔습니다. 도구는 설치하지 않고 개념만 씁니다. 나중에 도구로 옮겨가더라도 같은 단계 이름을 그대로 씁니다.

- `Spec Kit` [https://github.com/github/spec-kit](https://github.com/github/spec-kit)
- `Spec-Driven Development 강의 자료` [https://github.com/https-deeplearning-ai/sc-spec-driven-development-files](https://github.com/https-deeplearning-ai/sc-spec-driven-development-files)
- `define-goal` [https://github.com/openai/skills/tree/main/skills/.curated/define-goal](https://github.com/openai/skills/tree/main/skills/.curated/define-goal)
