# Goals

세 단계를 순서대로 진행합니다. 각 단계가 화면 하나로 끝납니다.

- [01. 환자 기본 뷰](./01-patient-view.md)
- [02. 도메인 뷰](./02-domain-view.md)
- [03. 시간축 뷰](./03-timeline-view.md)

각 파일은 OpenAI [`define-goal`](https://github.com/openai/skills/tree/main/skills/.curated/define-goal) 기준에 맞춰 그 단계의 목표, 증명 방법, 성공 기준을 담습니다. 아래 세 항목은 세 단계에 공통으로 적용됩니다.

## 어디까지가 범위인가

- React, TypeScript, Vite를 쓴다.
- `01-B-emr-viewer-goal/`을 그대로 프로젝트 루트로 사용한다.
- 상시 실행되는 백엔드와 API key 없이 동작한다.

범위 밖:

- `app/`이나 `frontend/` 하위 프로젝트
- 상시 실행되는 백엔드
- 인증과 권한 관리
- 챗봇이나 Text-to-SQL
- 원본 ZIP 수정

## 무엇을 만나면 멈추고 물어야 하는가

- 원본 ZIP을 수정해야 할 것 같을 때
- 성공 기준 중 하나를 완화해야 할 것 같을 때
- 그 단계의 목표에 없는 기능을 추가해야 할 것 같을 때
- 범위 밖으로 지정한 의존성이 필요하다고 판단될 때

## 참고 자료

- 입력은 `data/mimic-iv-clinical-database-demo-2.2.zip` 하나다.
- 비식별화된 환자 100명 부분집합이고, 임상 테이블 31개가 들어 있다. `hosp` 22개, `icu` 9개.
- 자유 서술형 임상 노트는 없다.
- ZIP 안에 `README.txt`, `LICENSE.txt`, `SHA256SUMS.txt`가 있다.
- ZIP의 SHA-256은 `97301a03820e8f41af211cf3462ddc19aefe75bbed05f11753859affaafeb8ec`다.
- 데이터셋 상세: <https://doi.org/10.13026/07hj-2a80>
- ODC Open Database License(ODbL)로 배포된다.
- 교육과 연구 프로토타이핑용이다. 임상 의사결정에 쓰지 않는다.
