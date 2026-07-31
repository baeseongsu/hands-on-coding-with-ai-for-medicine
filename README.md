# Coding with AI for Medicine: Hands-on Applications Workshop

이 저장소는 Codex와 같은 AI coding agent로 의료 AI 애플리케이션을 설계하고 구현하는 실습 프로젝트 모음입니다.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/baeseongsu/hands-on-coding-with-ai-for-medicine?quickstart=1)

각 프로젝트는 독립적인 작업 단위입니다. 디렉터리 번호는 실습 세션 순서를 나타내며, 선수 조건이나 코드 의존성을 뜻하지 않습니다. 원하는 프로젝트 하나만 진행해도 되고 여러 개를 병행해도 됩니다.

## 목차

- [프로젝트](#프로젝트)
- [시작하기](#시작하기)
  - [GitHub Codespaces에서](#github-codespaces에서)
  - [내 컴퓨터에서](#내-컴퓨터에서)
- [실습 환경](#실습-환경)
- [저장소 규칙](#저장소-규칙)
- [참고 자료](#참고-자료)
- [만든 사람](#만든-사람)
- [라이선스와 서드파티 데이터](#라이선스와-서드파티-데이터)
- [유의사항](#유의사항)

## 프로젝트

- `세션 I. Vibe Coding`: MIMIC-IV Demo로 EMR Data Viewer를 만듭니다. 같은 과제를 세 가지 방식으로 진행하고 결과를 비교합니다.
- `세션 II. Large Language Model`: 임상 도메인 LLM fine-tuning [[프로젝트]](./projects/02-clinical-domain-llm-finetuning/)
- `세션 III. AI Agent`: 데이터베이스와 Knowledge Graph에 대한 multi-agent reasoning [[프로젝트]](./projects/03-multi-agent-database-knowledge-graph/)

세션 I의 세 트랙을 가르는 것은 "끝났다"를 누가 판정하는가입니다.

| 트랙 | 진행 방식 | 완료 판정 |
|---|---|---|
| [A · vibe coding](./projects/01-A-emr-viewer-vibe/) | 계속 만들어달라고 합니다 | 사람이 화면을 보고 |
| [B · 목표 기반](./projects/01-B-emr-viewer-goal/) | 목표와 정지 조건만 주고 `/goal`에 맡깁니다 | 에이전트가 스스로 |
| [C · 명세 기반](./projects/01-C-emr-viewer-spec/) | 스펙과 완료 기준을 직접 씁니다 | 미리 정한 기준으로 사람이 |

한 사람이 세 트랙을 다 하는 것이 아닙니다. 하나를 골라 진행하고 마지막에 서로의 결과를 비교합니다.

스타터 패키지는 세션 I에만 있습니다. 세션 II와 III는 각 주제로 자유롭게 작업할 수 있는 공간입니다.

## 시작하기

### GitHub Codespaces에서

위 배지나 GitHub의 `Code` 버튼으로 Codespace를 만듭니다. Node, Python, Codex CLI가 이미 설치되어 있어서 따로 설정할 것이 없습니다.

터미널이 열리면 API key를 설정합니다. 강사가 passphrase를 알려주거나 key 자체를 배포하는데, 어느 명령을 쓸지는 터미널 안내 메시지에 표시됩니다. 입력은 한 번만 받으며, 화면에 표시되지 않고 셸 history에도 남지 않습니다.

```bash
bash .devcontainer/unlock-key.sh     # 강사가 passphrase를 알려준 경우
bash .devcontainer/set-api-key.sh    # 강사가 key를 직접 준 경우
```

그다음 새 터미널을 열고, 진행할 트랙으로 이동합니다. 어느 트랙인지는 강사가 안내합니다.

```bash
cd projects/01-A-emr-viewer-vibe    # 또는 01-B-emr-viewer-goal, 01-C-emr-viewer-spec
```

여기서부터는 그 트랙의 `README.md`가 안내합니다. 트랙마다 진행 방식이 다릅니다.

### 내 컴퓨터에서

```bash
git clone https://github.com/baeseongsu/hands-on-coding-with-ai-for-medicine.git
cd hands-on-coding-with-ai-for-medicine/projects/01-C-emr-viewer-spec
```

Codespaces 밖에서는 Node, Python, Codex CLI를 직접 설치하고 인증해야 합니다. 필요한 항목은 각 프로젝트의 `README.md`에 정리되어 있습니다.

어느 쪽이든 시작 전에 해당 프로젝트 디렉터리의 `README.md`를 먼저 읽으세요.

## 실습 환경

Codespaces 환경은 미리 설치되어 있고 모든 수강생에게 동일합니다.

- `Node.js` 22. 세션 I 애플리케이션 스택의 런타임입니다.
- `Python` 3.12. 가상환경 하나가 항상 활성 상태이므로 `activate` 단계가 없습니다.
- `Codex CLI`. prebuild 시점에 설치되며 인증은 되어 있지 않습니다.

프로젝트 공통 Python 패키지는 `.devcontainer/requirements-base.txt`에 선언합니다. 특정 프로젝트에만 필요한 패키지는 `projects/<세션>-<프로젝트>/requirements.txt`에 선언하며, 이 파일들은 모두 같은 가상환경에 설치됩니다.

저장소와 Codespace 이미지에는 평문 자격증명이 들어 있지 않습니다. 수강생이 수업 시작 시 각자 key를 설정합니다.

## 저장소 규칙

- 각 `projects/<세션>-<프로젝트>/` 디렉터리는 독립적인 프로젝트 루트입니다.
- 각 프로젝트는 자신의 문서, 소스 코드, 환경, 데이터, 자산을 스스로 관리합니다. Codespaces에서 Python 런타임은 공유하지만, 의존성은 각 프로젝트가 자기 `requirements.txt`에 선언합니다.
- 프로젝트 안에 `app/`이나 `frontend/` 같은 중첩 애플리케이션 프로젝트를 만들지 않습니다.
- 한 프로젝트가 다른 프로젝트의 소스 코드나 생성 산출물에 의존하게 만들지 않습니다.
- API key, `.env` 파일, 자격증명, 환자 식별 정보는 절대 커밋하지 않습니다.
- 이미지나 데이터 등 외부 자산을 추가할 때는 출처와 이용 조건을 함께 기록합니다.
- 이 수강생용 저장소에는 완성된 모범 답안이 포함되지 않습니다.
- 의료 AI 산출물은 교육과 연구 프로토타이핑 목적이며, 실제 임상 의사결정용이 아닙니다.

## 참고 자료

- `MIMIC-IV Demo` [https://physionet.org/content/mimic-iv-demo/2.2/](https://physionet.org/content/mimic-iv-demo/2.2/)
- `Codex` [https://developers.openai.com/codex/](https://developers.openai.com/codex/)
- `GitHub Codespaces` [https://docs.github.com/en/codespaces](https://docs.github.com/en/codespaces)
- `Dev Containers` [https://containers.dev/](https://containers.dev/)
- `React` [https://react.dev/](https://react.dev/)
- `Vite` [https://vite.dev/](https://vite.dev/)

## 만든 사람

- 배성수 (seongsu@kaist.ac.kr)

## 라이선스와 서드파티 데이터

이 저장소를 위해 작성된 코드와 문서는 MIT License를 따릅니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참고하세요.

MIMIC-IV Clinical Database Demo를 포함한 서드파티 데이터셋은 각자의 라이선스를 따릅니다. 세션 I 세 트랙의 `data/`에 들어 있는 ZIP은 같은 파일이며 ODC Open Database License(ODbL)로 배포됩니다. 재사용하거나 재배포하기 전에 ZIP에 포함된 `LICENSE.txt`와 출처 표기 요건을 확인하세요.

## 유의사항

- 이 저장소의 모든 자료는 연구와 교육 목적으로만 제공됩니다.
- 임상 데이터나 환자 식별 정보는 포함되어 있지 않습니다. 포함된 데이터셋은 비식별화된 공개 demo입니다.
- 여기서 만든 애플리케이션은 임상 시스템이 아니며, 진단, 예후 판정, 임상 의사결정 지원에 사용해서는 안 됩니다.
- 실제 임상 환경에 적용하기 전에 개인정보, 보안, 윤리 가이드라인을 반드시 확인하세요.
- 이 저장소의 기여자는 임상적 결과나 자료의 오용에 대해 어떠한 책임도 지지 않습니다.
