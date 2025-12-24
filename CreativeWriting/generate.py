import lmstudio as lms
import csv
import ast
import re
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

def generate_thinking(prompts:list[str]):
    llm_response = []
    data_length = len(prompts)
    for i,line in enumerate(prompts,1):
        result = llm_instance(line)
        response = replace_thinking(result.content.strip())
        llm_response.append(response)
        print(f"{i}/{data_length} generated")
        print(f"Prompt Tokens: {result.stats.prompt_tokens_count}")
        print(f"Predicted Tokens: {result.stats.predicted_tokens_count}\n\n")

    return llm_response

def llm_instance(prompt:str):
    with lms.Client() as client:
        model = client.llm.model("qwen3-14b")
        chat = lms.Chat()
        chat.add_user_message(prompt)
        result = model.respond(chat)
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
    responses = generate_thinking(generation_prompt)
    writer_csv(generation_prompt, prompts, responses, "writing-thinking.csv")

if __name__ == "__main__":
    main()
