import lmstudio as lms
import csv
import ast
import re
import time
import os
from prompts import PROMPTS

def read_csv(file:str):
    prompts = []
    generation_prompt = []

    with open(file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            essay_prompt = process_line(row["conversations"])
            prompts.append(essay_prompt)
            prompts_str = PROMPTS["creative_writing"] + "Prompt: " + essay_prompt
            generation_prompt.append(prompts_str)
    
    return prompts, generation_prompt

def process_line(input: str):
    line = ast.literal_eval(input.strip())
    return line[0].get("value")

def generate_thinking(generation_prompts:list[str], prompts:list[str], output:str, checkpoint:int=0):
    data_length = len(prompts)

    if not os.path.exists(output):
        with open(output, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["generation-prompt","prompt","response"])

    start_idx = checkpoint

    for i in range(start_idx, len(generation_prompts)):
        result = llm_instance(generation_prompts[i])
        response = replace_thinking(result.content.strip())

        with open(output, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([generation_prompts[i], prompts[i], response])

        print(f"{i+1}/{data_length} generated and saved")
        print(f"Prompt Tokens: {result.stats.prompt_tokens_count}")
        print(f"Predicted Tokens: {result.stats.predicted_tokens_count}\n\n")

def llm_instance(prompt:str):
    with lms.Client() as client:
        model = client.llm.model("qwen3-14b", config={"contextLength": 10240})
        result = model.respond(prompt)
        model.unload()
        time.sleep(1)
    return result

def replace_thinking(response:str):
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()

def writer_csv(gen_prompts:list[str], prompts:list[str], llm_response:list[str], output:str):
    header = [
        "generation-prompt",
        "prompt",
        "response"
    ]
    with open (output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(zip(gen_prompts, prompts, llm_response))

    print("Wrote file")

def main():
    prompts, generation_prompt = read_csv("./CreativeWriting/writing-prompt.csv")
    generate_thinking(generation_prompt, prompts, "./CreativeWriting/writing-thinking.csv", 3757)
    print("Generation complete!")

if __name__ == "__main__":
    main()
