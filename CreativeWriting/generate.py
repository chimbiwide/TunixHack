import lmstudio as lms
import csv
import ast
import re
from prompts import PROMPTS

def read_csv(file:str):
    prompts = []

    with open(file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            essay_prompt = process_line(row["conversations"])
            prompts_str = PROMPTS["creative_writing"] + "Prompt: " + essay_prompt
            prompts.append(prompts_str)
    
    return prompts

def process_line(input: str):
    line = ast.literal_eval(input.strip())
    return line[0].get("value")

def generate_thinking(prompts:list[str]):
    model = lms.llm("qwen3-14b")
    llm_response = []
    data_length = len(prompts)
    for i,line in enumerate(prompts,1):
        response = replace_thinking(model.respond(line).content.strip())
        llm_response.append(response)
        if i > 3:
            break
        print(f"{i}/{data_length} generated")

    return llm_response


def replace_thinking(response:str):
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()

def writer_csv(prompts:list[str], llm_response:list[str], output:str):
    header = [
        "prompt",
        "response"
    ]
    with open (output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(zip(prompts, llm_response))

    print("Wrote file")

def main():
    prompts = read_csv("./CreativeWriting/writing-prompt.csv")
    responses = generate_thinking(prompts)
    writer_csv(prompts, responses, "writing-thinking.csv")

if __name__ == "__main__":
    main()
