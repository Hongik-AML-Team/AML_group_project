# !pip install ace_tools_open (터미널에서 실행행)
import ace_tools_open as tools
from collections import Counter
import pandas as pd
import re, sys, os

# Ensure ace_tools is available if needed for display_dataframe_to_user
# Assuming ace_tools is in the AML_group_project directory
project_dir = "/content/AML_group_project"
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Define a placeholder if ace_tools is not found, to avoid NameError later
display_dataframe_to_user = None
try:
    from ace_tools import display_dataframe_to_user
except ModuleNotFoundError:
    print("Warning: ace_tools module not found. display_dataframe_to_user will not be available.")
    # display_dataframe_to_user remains None


# 오류 유형 분류 함수
def categorize_error(msg):
    """Categorizes error messages into common types."""
    if msg is None:
        return "오류 메시지 없음"
    msg = str(msg).lower() # Ensure message is a string and lowercased for easier matching
    if "unexpected eof" in msg or "unterminated" in msg or "eof while parsing" in msg:
        return "괄호/따옴표 안 닫힘 (EOF 오류)"
    elif "invalid syntax" in msg:
        return "문법 오류"
    elif "unindent does not match" in msg or "expected an indented block" in msg:
        return "들여쓰기 오류"
    elif "is not defined" in msg or "name '" in msg and "' is not defined" in msg:
        return "변수/함수명 오류"
    elif "indexerror" in msg or "list index out of range" in msg:
        return "인덱싱 오류"
    elif "typeerror" in msg:
        return "타입 오류"
    elif "attributeerror" in msg:
        return "속성 오류"
    elif "keyerror" in msg:
        return "키 오류"
    elif "valueerror" in msg:
        return "값 오류"
    elif "zerodivisionerror" in msg:
        return "0 나누기 오류"
    else:
        return "기타"

# JSONL 파일 로드 및 오류 분류
failures = []
# Initialize df to an empty DataFrame before the try block
df = pd.DataFrame()
results_dir = os.path.join(project_dir, "results")
failures_file = os.path.join(results_dir, "compile_failures.jsonl")

print(f"Attempting to load compilation failures from: {failures_file}")

try:
    if os.path.exists(failures_file) and os.path.getsize(failures_file) > 0:
        with open(failures_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    error_type = categorize_error(entry.get("error")) # Pass the error message to the categorizer
                    failures.append({
                        "입력 설명 (src)": entry.get("src", "N/A"), # Use .get with default to handle missing keys
                        "예상 정답 (tgt)": entry.get("tgt", "N/A"),
                        "모델 출력 (pred)": entry.get("pred", "N/A"),
                        "오류 메시지": entry.get("error", "N/A"),
                        "오류 유형": error_type
                    })
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {line.strip()} - Error: {e}")
        # Create DataFrame from failures list if file was read successfully and had data
        if failures:
            df = pd.DataFrame(failures)
        else:
            print("The compile_failures.jsonl file was empty or contained no valid JSON lines.")

    else:
        print("Error: compile_failures.jsonl not found or is empty.")
        print(f"Expected file at: {failures_file}")
        # df remains an empty DataFrame initialized before the try block

except Exception as e: # Catch other potential errors during file processing
    print(f"An error occurred while processing {failures_file}: {e}")
    # df remains an empty DataFrame

# Check if the DataFrame is not empty before proceeding with analysis and display
if not df.empty:
    # 오류 유형별 개수 요약
    # Ensure the '오류 유형' column exists before calling value_counts
    if '오류 유형' in df.columns:
        summary = df["오류 유형"].value_counts().reset_index()
        summary.columns = ["오류 유형", "발생 횟수"]
    else:
        print("Error: '오류 유형' column not found in the DataFrame. Cannot generate summary.")
        summary = pd.DataFrame(columns=["오류 유형", "발생 횟수"]) # Create empty summary if column is missing


    # Display the full failure details DataFrame
    # Only attempt to display if ace_tools was imported and df is not empty
    if display_dataframe_to_user is not None:
        print("\n--- Detailed Failure Cases ---")
        display_dataframe_to_user(name="오류 케이스 상세", dataframe=df)
    else:
         print("\n--- Detailed Failure Cases (display_dataframe_to_user not available) ---")
         print(df.to_string()) # Fallback to printing the DataFrame


    # --- Generate Structured Report ---
    print("\n# 모델 컴파일 오류 분석 보고서\n")

    print("## 1. 오류 유형별 통계\n")
    # Use to_markdown for a nice table format
    # Check if summary has columns before trying to convert
    if not summary.empty:
        print(summary.to_markdown(index=False))
    else:
        print("No summary data available.")
    print("\n")

    # Proceed with detailed examples only if df is not empty and has the necessary columns
    if not df.empty and '오류 유형' in df.columns:
        print("## 2. 오류 유형별 상세 예시 및 분석\n")

        for index, row in summary.iterrows():
            error_type = row["오류 유형"]
            count = row["발생 횟수"]

            print(f"### 2.{index+1}. {error_type} ({count}건)\n")

            # Get examples for this error type (e.g., first 3 examples)
            examples = df[df["오류 유형"] == error_type].head(3)

            for i, example_row in examples.iterrows():
                print(f"#### 예시 {i+1}\n")
                print("**입력 설명 (src):**")
                print(f"> {example_row['입력 설명 (src)']}\n")
                print("**모델 출력 (pred):**")
                print("python") 
                print(example_row['모델 출력 (pred)'])
                print("\n")
                # Optional: print target code for comparison
                # print("**예상 정답 (tgt):**")
                # print("python")

                # print(example_row['예상 정답 (tgt)'])
                # print("\n")
                print("**오류 메시지:**")
                print(f"> {example_row['오류 메시지']}\n")

                # Basic analysis and suggestion based on category
                print("**분석 및 개선 방향:**\n")
                if error_type == "괄호/따옴표 안 닫힘 (EOF 오류)":
                    print("- **원인:** 문장 끝에 괄호나 따옴표가 닫히지 않았거나, 블록이 제대로 끝나지 않음.")
                    print("- **개선:** 모델 학습 시 일관된 코드 포맷팅을 강화하거나, 후처리 단계에서 기본적인 괄호/따옴표 쌍 검사 로직 추가를 고려할 수 있습니다.")
                elif error_type == "문법 오류":
                     print("- **원인:** 파이썬 문법 규칙을 따르지 않은 코드 생성.")
                     print("- **개선:** 더 많은 양질의 코드 데이터로 학습하거나, 문법 검사기를 이용한 후처리를 적용할 수 있습니다.")
                elif error_type == "들여쓰기 오류":
                     print("- **원인:** 파이썬에서 중요한 들여쓰기가 잘못 적용됨.")
                     print("- **개선:** 모델이 코드 구조를 더 잘 이해하도록 아키텍처를 개선하거나, 들여쓰기 규칙에 기반한 후처리 로직을 적용해야 합니다.")
                elif error_type == "변수/함수명 오류":
                     print("- **원인:** 정의되지 않은 변수나 함수 이름 사용.")
                     print("- **개선:** 학습 데이터셋에 등장하는 변수/함수 이름의 다양성을 늘리거나, 흔히 사용되는 내장 함수/모듈 이름을 모델이 더 잘 인식하도록 학습 데이터를 보강해야 합니다.")
                elif error_type == "인덱싱 오류":
                     print("- **원인:** 시퀀스(리스트, 튜플 등)의 범위를 벗어나는 인덱스 사용.")
                     print("- **개선:** 모델이 데이터 구조와 접근 방식에 대한 이해도를 높이도록 학습 데이터를 조정하거나, 생성된 코드의 인덱스 유효성을 검사하는 후처리를 추가할 수 있습니다.")
                elif error_type == "타입 오류":
                     print("- **원인:** 연산이나 함수 호출 시 예상치 못한/호환되지 않는 데이터 타입 사용.")
                     print("- **개선:** 모델이 데이터 타입 간의 상호작용을 더 잘 학습하도록 데이터셋을 구성하거나, 기본적인 타입 힌트나 타입 검사 로직을 활용한 후처리를 고려할 수 있습니다.")
                elif error_type == "속성 오류":
                     print("- **원인:** 객체에 존재하지 않는 속성(메서드나 변수)에 접근하려고 함.")
                     print("- **개선:** 모델이 객체 지향 개념과 클래스/객체의 속성을 더 정확히 학습하도록 데이터를 보강하거나, API 문서/라이브러리 정보를 활용한 후처리를 적용할 수 있습니다.")
                elif error_type == "키 오류":
                     print("- **원인:** 딕셔너리에 존재하지 않는 키에 접근하려고 함.")
                     print("- **개선:** 딕셔너리 사용 패턴에 대한 학습을 강화하거나, 키 존재 여부를 확인하는 후처리 로직을 추가할 수 있습니다.")
                elif error_type == "값 오류":
                     print("- **원인:** 함수나 연산이 유효하지 않은 값이나 인수를 받았을 때 발생.")
                     print("- **개선:** 유효한 값의 범위를 모델이 더 잘 이해하도록 학습 데이터를 조정하거나, 입력 값의 유효성을 검사하는 후처리를 적용할 수 있습니다.")
                elif error_type == "0 나누기 오류":
                     print("- **원인:** 숫자를 0으로 나누려고 함.")
                     print("- **개선:** 0으로 나누는 상황을 피하는 패턴을 학습하거나, 나누기 연산 전에 분모가 0인지 확인하는 후처리 로직을 추가할 수 있습니다.")
                else: # 기타
                     print("- **원인:** 위 범주에 속하지 않는 다양한 오류.")
                     print("- **개선:** 개별 오류 메시지를 상세히 검토하여 근본 원인을 파악하고, 해당 패턴을 줄일 수 있는 데이터나 모델 개선 방향을 모색해야 합니다.")

                print("---\n") # Separator for examples

        # Optional: General suggestions for improvement
        print("## 3. 종합 개선 방안\n")
        print("- **데이터 증강:** 다양한 형태의 문법적으로 올바른 코드와 일부러 오류를 포함시킨 코드 쌍을 학습 데이터에 추가하여 모델의 오류 감지 및 수정 능력을 향상시킬 수 있습니다.")
        print("- **후처리 파이프라인:** 생성된 코드에 대해 문법 검사(linter)나 정적 분석 도구를 적용하여 흔한 오류 패턴을 자동으로 수정하거나 플래그 지정하는 후처리 단계를 도입하는 것을 고려합니다.")
        print("- **모델 아키텍처/ 학습:** 오류 유형별 분포를 분석하여 모델이 특정 유형의 오류를 자주 생성하는 경우, 해당 유형에 취약한 부분을 보완하는 모델 아키텍처 변경이나 학습 전략 수정을 시도할 수 있습니다.")

    elif not df.empty and '오류 유형' not in df.columns:
         print("\nCould not generate detailed report because '오류 유형' column is missing.")
    else:
        print("\nNo failure data loaded from results/compile_failures.jsonl.")
        print("Please ensure the file exists, is not empty, contains valid JSON lines, and the evaluation script was run successfully.")