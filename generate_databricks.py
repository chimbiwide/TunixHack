import lmstudio as lms
import json
import re
import csv
import time
from prompts import PROMPTS

def process_file(filename: str):
    data = []
    categories = []
    prompts = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            currentLine = json.loads(line)
            current_sys_prompt = create_system_prompt(currentLine)
            data.append(current_sys_prompt)
            categories.append(currentLine.get("category"))
            prompts.append(currentLine.get("instruction"))
    return data, categories, prompts

def create_system_prompt(currentLine):
    prompt = currentLine.get("instruction")
    context = currentLine.get("context")
    response = currentLine.get("response")
    category = currentLine.get("category")
    sys_prompt = PROMPTS.get(category) + "Prompt: " + prompt
    match category:
        case "summarization":
            sys_prompt += "\nContext: " + context
        case "closed_qa":
            sys_prompt += "\nContext: " + context
        case "open_qa":
            sys_prompt += "\nCorrect Answer: " + response
        case "information_extraction":
            sys_prompt += "\nSupplementary Text: " + context
        case "classification":
            sys_prompt += "\nCorrect Answer: " + response
    return sys_prompt

def generate_responses(data:list[str]):
    model = lms.llm("qwen3-14b")
    data_length = len(data)
    llm_response = []
    start_time = time.time()
    for i, prompt in enumerate(data,1):
       response = replace_thinking(model.respond(prompt).content).strip()
       print_status(start_time, i, data_length)
       llm_response.append(response)

    total_time = time.time() - start_time
    print(f"\n\n\n Total Generation Time: {total_time/60:.2f} minutes")
    return llm_response

def print_status(start_time, i, data_length):
   elapsed_time = time.time() - start_time

   days = int(elapsed_time // 86400)
   hours = int((elapsed_time % 86400) // 3600)
   mins = int((elapsed_time % 3600) // 60)
   secs = int(elapsed_time % 60)
   if days > 0:
       status = f"{days:02d}:{hours:02d}:{mins:02d}:{secs:02d}"
   else:
       status = f"{hours:02d}:{mins:02d}:{secs:02d}"
   print(f"Generated {i}/{data_length} responses | Elapsed: {status}")


def replace_thinking(response:str):
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)

def write_csv(gen_prompt:list[str], response:list[str], categories:list[str], prompts:list[str], outputfilename:str):
    with open(outputfilename, 'w', newline='')  as f:
        writer = csv.writer(f)
        header = ["Generation Prompt", "Prompt", "Model_Response", "Categories"]
        writer.writerow(header)
        writer.writerows(zip(gen_prompt, prompts, response, categories))

def main():
    data, categories, prompts = process_file("databricks.jsonl")
    responses = generate_responses(data)
    write_csv(data, responses, categories, prompts, "databricks_with_reason.csv")

if __name__ == "__main__":
    main()