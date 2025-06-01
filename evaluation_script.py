import json
import torch
from tqdm import tqdm
from transformers import AutoConfig, AutoTokenizer, AutoModelForSeq2SeqLM, T5ForConditionalGeneration

import sacrebleu

def evaluate():
    """
    Evaluates a fine-tuned CodeT5-base model by calculating compile success rate and BLEU score.
    """
    
    model_dir = "./best_model"
    # Load model configuration and tokenizer
    try:
        config = AutoConfig.from_pretrained(model_dir, local_files_only=True)
        tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
        
        # Load the model architecture from the configuration
        model = T5ForConditionalGeneration(config)
        
        # Load the model checkpoint from the saved files
        model_checkpoint_path = f"{model_dir}/pytorch_model.bin" # Assuming the checkpoint file is named pytorch_model.bin
        model.load_state_dict(torch.load(model_checkpoint_path, map_location=torch.device('cuda')))
        
    except Exception as e:
        print(f"Error loading model or tokenizer: {e}")
        print("Please ensure 'best_model' directory exists and contains valid model files.")
        return

    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Load evaluation data
    try:
        with open("conala_valid.jsonl", "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f]
    except FileNotFoundError:
        print("Error: conala_valid.jsonl not found.")
        print("Please ensure conala_valid.jsonl is in the same directory.")
        return

    # Prepare for batch evaluation
    batch_size = 8
    preds, refs = [], []
    compile_ok = 0

    # Iterate in batches for generation and compilation check
    for i in tqdm(range(0, len(data), batch_size), desc="Evaluating"):
        batch = data[i : i + batch_size]
        nls = [ex["src"] for ex in batch]
        tgts = [ex["tgt"] for ex in batch]

        inputs = tokenizer(
            nls,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        ).to(device)

        with torch.no_grad():
            outs = model.generate(
                **inputs,
                max_length=128,
                num_beams=8,
                early_stopping=True
            )

        batch_preds = [tokenizer.decode(o, skip_special_tokens=True) for o in outs]
        preds.extend(batch_preds)
        refs.extend(tgts)

        for pred in batch_preds:
            try:
                compile(pred, "<string>", "exec")
                compile_ok += 1
            except Exception:
                pass # Ignore compilation errors for now

    # Calculate BLEU score and print results
    if len(preds) > 0 and len(refs) > 0:
        bleu = sacrebleu.corpus_bleu(preds, [refs]).score
        total = len(data)

        print("\n===== Evaluation Results =====")
        print(f"Sample count           : {total}")
        print(f"Compile success rate   : {compile_ok}/{total} ({compile_ok/total*100:.1f}%)")
        print(f"BLEU score             : {bleu:.2f}")
    else:
        print("\nNo predictions generated. Evaluation cannot be completed.")


if __name__ == "__main__":
    evaluate()