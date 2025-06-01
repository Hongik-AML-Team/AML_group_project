# 🔍 CodeT5 기반 자연어-코드 변환 모델 평가 및 검증 보고서

## 1. 프로젝트 개요

본 프로젝트는 기계학습심화 팀 프로젝트의 일환으로, 자연어로 주어진 프로그래밍 요구사항을 파악하고 이에 상응하는 파이썬 코드를 생성하는 모델을 구축하고자 하였다. 본인은 팀에서 파인튜닝된 CodeT5 모델의 **성능 평가 및 오류 분석**을 담당하였다.

## 2. 사용 모델 및 학습 환경

- **모델 아키텍처**: CodeT5 (base)
- **사전 학습 모델**: Salesforce/codet5-base
- **파인튜닝 데이터셋**: CoNaLa (train 2,379개 / valid 500개)
- **모델 저장 경로**: `./best_model/`
- **토크나이저 구성 파일**: tokenizer_config.json, vocab.json, merges.txt 등

## 3. 평가 방법

### 3.1 정량 평가 스크립트 (`evaluation_script.py`)

- `conala_valid.jsonl`을 기반으로 평가
- 입력: 자연어 질의 (`src`)
- 출력: 모델 생성 코드
- 참조: `tgt` 코드
- **평가 지표**: BLEU score (sacrebleu 기반)
- 결과 저장 없음 (BLEU 및 샘플 출력만 프린트)

### 3.2 컴파일 실패 케이스 분석 (`analyze_compilation_failures.py`)

- `results/compile_failures.jsonl`에 기록된 실패 케이스 자동 분석
- 주요 실패 유형 분류 및 수치화
- 분석 결과는 `compilation_failure_analysis.md`에 요약 정리됨

## 4. 평가 결과

### 4.1 BLEU 점수

- **평균 BLEU score**: 17.70

### 4.2 컴파일 성공률

- **총 샘플 수**: 500
- **성공**: 481
- **실패**: 19
- **성공률**: 96.2%

## 5. 오류 분석 요약

- 총 19건의 컴파일 실패 케이스를 분석한 결과는 다음과 같음:

| 오류 유형 | 건수 | 비고 |
|-----------|------|------|
| SyntaxError | 8건 | 괄호 누락, 잘못된 들여쓰기 등 |
| NameError | 6건 | 정의되지 않은 변수 사용 |
| TypeError | 3건 | 연산자 타입 불일치 등 |
| 기타 | 2건 | 예외적으로 발생한 에러 |

- 상세 분석은 `compilation_failure_analysis.md` 참고

## 6. 결론 및 향후 과제

### 결론

- BLEU 점수는 낮게 나왔으나, 컴파일 성공률은 매우 높은 편으로 **구문적으로 유효한 코드 생성 능력**은 우수함
- BLEU 기반 평가는 정답과 생성 코드 간 문자열 일치를 기반으로 하기 때문에 코드 의미를 온전히 반영하지 못하는 한계가 있음

### 개선 방안

- **BLEU 외 정성 평가 지표 도입 필요**
- **테스트 케이스 기반 실행 평가 추가 고려**
- **자연어 조건이 포함된 입력 다양화**를 통한 데이터 일반화 필요

## 7. 부록

### 실행 예시 (평가 스크립트)

```bash
python evaluation_script.py
```

### 생성 코드 예시

질문: *Decode Hex String in Python 3*  
참조: `bytes.fromhex('4a4b4c').decode('utf-8')`  
생성: `. public static String`

→ 문자열로 유사해 보이나 전혀 다른 언어(Java)로 출력되어 BLEU 점수 낮음

### 분석 스크립트 실행 예시

```bash
python analyze_compilation_failures.py
```

결과 요약은 `compilation_failure_analysis.md`에 저장됨

---

🧾 본 README는 모델 평가 결과를 바탕으로, 모델의 한계 및 개선 방향을 정리한 문서임. 발표 및 제출용 보고서로 활용 가능.
