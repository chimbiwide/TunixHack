import lmstudio as lms
import json
import re
import csv
from prompts import PROMPTS

def process_file(filename: str):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            currentLine = json.loads(line)
            current_sys_prompt = create_system_prompt(currentLine)
            data.append(current_sys_prompt)
    return data

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
    for i, prompt in enumerate(data,1):
       response = replace_thinking(model.respond(prompt).content).strip()
       print(f"Generated {i}/{data_length} responses")
       llm_response.append(response)
       if (i == 10):
           break
    return llm_response

def replace_thinking(response:str):
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)

def write_csv(prompt:list[str], response:list[str], outputfilename:str):
    with open(outputfilename, 'w', newline='')  as f:
        writer = csv.writer(f)
        header = ["Prompt", "Model_Response"]
        writer.writerow(header)
        writer.writerows(zip(prompt, response))

def main():
    data = process_file("databricks.jsonl")
    responses = generate_responses(data)
    write_csv(data, responses, "databricks_with_reason.csv")

if __name__ == "__main__":
    main()