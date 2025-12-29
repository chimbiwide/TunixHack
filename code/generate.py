import csv, re
import time
import os
import lmstudio as lms

code = """
You will be given a python coding problem and the correct answer. Generate the reasoning traces that get to the final answer.
Your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
Do not reference that the correct answer is provided in the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
"""
def read_csv(filename:str):
    question = []
    answer = []

    with open(filename, 'r') as f:
        file = csv.DictReader(f)
        for line in file:
            question.append(line.get("prompt"))
            answer.append(line.get("code"))
    return question, answer

def create_prompt(q:list[str], a:list[str]) -> list[str]:
    prompts = []
    for question,answer in zip(q,a):
        prompt = f"{code} Prompt:{question} Correct Code:{answer}"
        prompts.append(prompt)
    return prompts

def replace_thinking(response:str):
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()

def generate_thinking(generation_prompts:list[str],prompts:list[str], output:str, checkpoint:int=0):
    data_length = len(prompts)
    header = ["generation_prompt", "prompt", "response"]

    if not os.path.exists(output):
        with open (output, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    start_idx = checkpoint

    for i in range (start_idx, len(generation_prompts)):
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
        time.sleep(0.5)
    return result


def write_csv(generation_prompt:list[str], prompt:list[str],response:list[str], output:str):
    header = ["generation_prompt", "prompt", "response"]
    with open(output,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(zip(generation_prompt, prompt, response))
    print("Wrote file")

def main():
    question, answer = read_csv("./code/code.csv")
    generation_prompt = create_prompt(question, answer)
    generate_thinking(generation_prompt,question,"./code/code-thinking.csv", 171)

if __name__ == "__main__":
    main()
