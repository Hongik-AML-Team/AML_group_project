import torch
import numpy as np
from datasets import load_dataset
import evaluate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer, get_linear_schedule_with_warmup

# 1) 데이터 로드
dataset = load_dataset("json", data_files={"train":"conala_train.jsonl","valid":"conala_valid.jsonl"})

# 데이터셋 구조 확인
print("데이터셋 구조:")
print(dataset["train"][0])  # 첫 번째 샘플 출력

# 더 큰 모델 사용 (small -> base)
model_name = "Salesforce/codet5-base"  # small 대신 base 모델 사용
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 최대 길이 증가
max_source_length = 256  # 128 -> 256
max_target_length = 256  # 128 -> 256

def preprocess(batch):
    # conala 데이터셋은 "src"(질문)와 "tgt"(코드) 형식으로 구성되어 있습니다
    # 데이터셋이 이미 딕셔너리 형태로 로드되었으므로 직접 접근
    inp = batch["src"]
    tgt = batch["tgt"]
    
    # 소스 텍스트 토큰화 - 최대 길이 증가
    model_inputs = tokenizer(inp, truncation=True, padding="max_length", max_length=max_source_length)
    
    # 타겟 코드 토큰화 - 최대 길이 증가
    labels = tokenizer(tgt, truncation=True, padding="max_length", max_length=max_target_length).input_ids
    
    # labels에서 패딩 토큰을 -100으로 설정 (손실 계산 시 무시)
    for i in range(len(labels)):
        labels[i] = [l if l != tokenizer.pad_token_id else -100 for l in labels[i]]
    
    model_inputs["labels"] = labels
    return model_inputs

# 데이터셋 토큰화 및 전처리
tokenized = dataset.map(preprocess, batched=True, remove_columns=["src", "tgt"])

# 2) 모델 로드 - 더 큰 모델 사용
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# 3) 트레이닝 아규먼츠 - 성능 향상을 위한 매개변수 조정
args = Seq2SeqTrainingArguments(
    output_dir="ckpt",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=5,  # 2 -> 5 에포크로 증가
    learning_rate=5e-5,  # 명시적 학습률 설정
    weight_decay=0.01,   # 가중치 감쇠 추가
    logging_steps=100,
    save_steps=200,
    save_total_limit=3,  # 2 -> 3으로 증가
    predict_with_generate=True,
    generation_max_length=max_target_length,  # 생성 최대 길이 설정
    generation_num_beams=8,  # 빔 크기 5 -> 8로 증가
)

# BLEU 점수 계산을 위한 메트릭 로드
metric = evaluate.load("sacrebleu")

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    # -100으로 마스킹된 레이블을 무시
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    
    # 생성된 토큰의 범위를 확인하고 유효한 범위로 제한
    max_token_id = len(tokenizer) - 1
    preds = np.clip(preds, 0, max_token_id)
    
    try:
        # 생성된 토큰을 텍스트로 디코딩
        decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
        
        # BLEU 점수 계산
        result = metric.compute(predictions=decoded_preds, references=[[l] for l in decoded_labels])
        result = {"bleu": result["score"]}
        
        # 생성 길이 추가
        prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
        result["gen_len"] = np.mean(prediction_lens)
        
        return result
    except Exception as e:
        print(f"디코딩 중 오류 발생: {e}")
        # 오류 발생 시 더미 결과 반환
        return {"bleu": 0.0, "gen_len": 0.0}

# 학습 스텝 계산
num_train_samples = len(tokenized["train"])
total_steps = int(num_train_samples / args.per_device_train_batch_size * args.num_train_epochs)
warmup_steps = int(0.1 * total_steps)  # 10% 워밍업

trainer = Seq2SeqTrainer(
    model=model,
    args=args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["valid"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# 4) 학습 실행
trainer.train()

# 5) 모델 평가
try:
    eval_results = trainer.evaluate()
    print(f"BLEU: {eval_results.get('eval_bleu', 0.0):.2f}")
except Exception as e:
    print(f"평가 중 오류 발생: {e}")

# 6) 모델 저장
trainer.save_model("./best_model")

# 7) 향상된 추론 예제
def generate_code(question):
    try:
        inputs = tokenizer(question, return_tensors="pt", truncation=True, padding="max_length", max_length=max_source_length)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # 향상된 코드 생성 매개변수
        outputs = model.generate(
            **inputs,
            max_length=max_target_length,
            num_beams=8,           # 5 -> 8로 증가
            early_stopping=True,
            temperature=0.7,        # 다양성을 위한 온도 조절
            top_p=0.9,              # 핵 샘플링 추가
            no_repeat_ngram_size=2  # 반복 방지
        )
        
        # 생성된 코드 디코딩
        generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_code
    except Exception as e:
        print(f"코드 생성 중 오류 발생: {e}")
        return "코드 생성에 실패했습니다."

# 테스트 코드 추가
test_questions = [
    "How to convert a list of integers to a single integer?",
    "How to reverse a list in Python?",
    "How to check if a string contains a substring?",
    "How to get current date and time in Python?"
]

print("\n=== 생성된 코드 예제 ===")
for question in test_questions:
    generated_code = generate_code(question)
    print(f"\n질문: {question}")
    print(f"생성된 코드: {generated_code}")
