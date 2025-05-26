# CodeT5를 활용한 자연어-코드 변환 모델 구현

## 프로젝트 개요

본 연구는 CodeT5-base 모델을 CoNaLa 데이터셋으로 파인튜닝하여 자연어 지시문을 Python 코드로 변환하는 모델을 개발하였습니다. 이 모델은 프로그래밍 학습자와 개발자의 코딩 생산성을 향상시키는 데 활용될 수 있습니다.

## 모델 다운로드

파인튜닝된 모델은 용량이 커서 GitHub에 포함되지 않았습니다. 아래 링크에서 다운로드 가능합니다:

- [파인튜닝된 모델 다운로드 (best_model.zip)](https://drive.google.com/file/d/1IGmot02uQmL0MLxD0sosqOA2tgjFLJZd/view?usp=sharing)

다운로드 후, 압축을 풀고 프로젝트 디렉토리에 `best_model` 폴더를 위치시키면 됩니다:

```bash
unzip best_model.zip -d .
```

## 데이터셋

CoNaLa(Code/Natural Language Challenge) 데이터셋을 사용하였습니다:
- **훈련 데이터**: 2,379개 자연어-코드 쌍
- **검증 데이터**: 500개 자연어-코드 쌍
- **데이터 형식**: `{"src": "자연어 질문", "tgt": "Python 코드"}`

## 모델 구조

- **기반 모델**: CodeT5-base (Salesforce)
- **모델 유형**: Sequence-to-Sequence Transformer
- **파라미터 수**: 약 220M
- **토크나이저**: RobertaTokenizerFast

## 파인튜닝 방법론

### 1. 전처리
- 소스/타겟 최대 길이: 256 토큰
- 라벨 패딩 처리: -100으로 마스킹 (손실 계산 제외)

### 2. 학습 설정
- **에포크**: 5
- **배치 크기**: 4
- **학습률**: 5e-5 (선형 감소)
- **옵티마이저**: AdamW
- **가중치 감쇠**: 0.01
- **워밍업**: 총 스텝의 10%

### 3. 평가 메트릭
- **BLEU**: 생성된 코드와 참조 코드 간의 유사도 측정
- **생성 길이**: 생성된 코드의 평균 토큰 수

### 4. 코드 생성 전략
- **빔 검색**: 빔 크기 8
- **온도**: 0.7
- **Top-p 샘플링**: 0.9
- **N-gram 반복 방지**: 2

## 실험 결과

### 학습 추이
| 에포크 | 손실   | 학습률          |
|--------|--------|-----------------|
| 0.17   | 2.6998 | 4.83e-5         |
| 1.01   | 1.8790 | 3.99e-5         |
| 2.02   | 1.4963 | 2.98e-5         |
| 3.03   | 1.1460 | 1.97e-5         |
| 4.03   | 0.9932 | 9.66e-6         |
| 5.00   | 0.8945 | 1.26e-6         |

**총 학습 시간**: 약 2시간 (7098초)

### 최종 성능
- **BLEU 점수**: 14.48
- **평균 생성 길이**: 측정됨 (구체적 값 보고 안됨)

### 코드 생성 예시
1. **질문**: How to convert a list of integers to a single integer?  
   **생성 코드**: `[int(x) for x in L]`

2. **질문**: How to reverse a list in Python?  
   **생성 코드**: `reversed(lst)`

3. **질문**: How to check if a string contains a substring?  
   **생성 코드**: `if (s.startswith('substring')): pass`

4. **질문**: How to get current date and time in Python?  
   **생성 코드**: `dt = datetime.datetime.now()`

## 분석 및 논의

### 성능 향상 요인
1. **모델 크기 확대**: CodeT5-small에서 base로 업그레이드 (60M → 220M 파라미터)
2. **학습 최적화**: 
   - 에포크 수 증가 (2 → 5)
   - 학습률 및 감쇠 최적화
3. **시퀀스 길이 확장**: 128 → 256 토큰
4. **생성 매개변수 조정**: 빔 크기, 온도, top-p 샘플링 등

### 한계점 및 개선 방향
1. **코드 정확성**: 일부 생성된 코드가 질문의 의도를 완전히 반영하지 못함
2. **다양성**: 더 복잡한 코딩 문제에 대한 검증 필요
3. **성능 개선 방안**:
   - 더 큰 데이터셋 활용
   - 모델 아키텍처 확장
   - 도메인 특화 사전 학습

## 사용 방법

### 필요 라이브러리
```bash
pip install torch<2.0.0 transformers<4.30.0 datasets evaluate sacrebleu numpy accelerate
```

### 모델 파인튜닝
```bash
python finetune.py
```

### 모델 추론
```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("./best_model")
model = AutoModelForSeq2SeqLM.from_pretrained("./best_model")

def generate_code(question):
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding="max_length", max_length=256)
    outputs = model.generate(
        **inputs, 
        max_length=256, 
        num_beams=8, 
        temperature=0.7,
        top_p=0.9,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 예시 사용법
question = "How to sort a dictionary by value in Python?"
code = generate_code(question)
print(f"생성된 코드: {code}")
```

## 결론

본 연구는 CodeT5 모델을 CoNaLa 데이터셋으로 파인튜닝하여 자연어를 Python 코드로 변환하는 모델을 성공적으로 개발하였습니다. BLEU 점수 14.48을 달성하였으며, 다양한 프로그래밍 질문에 대해 합리적인 코드를 생성할 수 있음을 확인하였습니다. 향후 연구에서는 더 큰 데이터셋과 모델을 활용하여 성능을 개선하고, 더 복잡한 프로그래밍 작업에 대한 코드 생성 능력을 향상시킬 계획입니다. 