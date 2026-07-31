# 01-A: EMR Viewer, vibe coding

MIMIC-IV Demo 데이터로 EMR Data Viewer를 만듭니다. 환자를 찾고 그 환자의 입원·진단·처방·검사를 볼 수 있는 로컬 웹 애플리케이션입니다.

## 목차

- [이 트랙의 방식](#이-트랙의-방식)
- [시작](#시작)
- [원본 데이터](#원본-데이터)

## 이 트랙의 방식

> There's a new kind of coding I call "vibe coding", where you fully give in to the vibes, embrace exponentials, and forget that the code even exists. It's possible because the LLMs (e.g. Cursor Composer w Sonnet) are getting too good. Also I just talk to Composer with SuperWhisper so I barely even touch the keyboard. I ask for the dumbest things like "decrease the padding on the sidebar by half" because I'm too lazy to find it. I "Accept All" always, I don't read the diffs anymore. When I get error messages I just copy paste them in with no comment, usually that fixes it. The code grows beyond my usual comprehension, I'd have to really read through it for a while. Sometimes the LLMs can't fix a bug so I just work around it or ask for random changes until it goes away. It's not too bad for throwaway weekend projects, but still quite amusing. I'm building a project or webapp, but it's not really coding - I just see stuff, say stuff, run stuff, and copy paste stuff, and it mostly works.
>
> Andrej Karpathy (@karpathy), 2025년 2월 3일

```text
Describe → Run → Revise → Describe → …
```

## 시작

```bash
cd projects/01-A-emr-viewer-vibe
codex
```

## 원본 데이터

- `data/mimic-iv-clinical-database-demo-2.2.zip`은 공개 배포되는 MIMIC-IV Clinical Database Demo v2.2입니다.
- 비식별화된 환자 100명 부분집합이고, 임상 테이블 31개가 들어 있습니다.
- 원본 ZIP을 수정하거나 덮어쓰지 마세요. 압축을 풀거나 변환한 결과는 별도 경로에 만드세요.
- ODC Open Database License(ODbL)로 배포됩니다. 데이터셋 상세는 <https://doi.org/10.13026/07hj-2a80>.
- 여기서 만든 것은 교육용이며 임상에 쓰지 않습니다.
