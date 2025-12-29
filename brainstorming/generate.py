import csv, re, time
import lmstudio as lms

brainstorming = """
You will be given a brainstorming idea. Generate the reasoning traces that get to the final answer.
your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
your final final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
"""
def read_csv(filename:str):
    question = []

    with open(filename, 'r') as f:
        file = csv.DictReader(f)
        for line in file:
            question.append(f"{line.get("input")} {line.get("instruction")}")
    return question

def create_prompt(q:list[str]) -> list[str]:
    prompts = []
    for question in q:
        prompt = f"{brainstorming} Prompt:{question}"
        prompts.append(prompt)
    return prompts

def replace_thinking(response:str):
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()

def generate_thinking(prompts:list[str]):
    llm_response = []
    data_length = len(prompts)
    for i,line in enumerate(prompts,1):
        result = llm_instance(line,i)
        response = replace_thinking(result.content.strip())
        llm_response.append(response)
        print(f"{i}/{data_length} generated")
        print(f"Prompt Tokens: {result.stats.prompt_tokens_count}")
        print(f"Predicted Tokens: {result.stats.predicted_tokens_count}\n\n")
    return llm_response

def llm_instance(prompt:str, i:int):
    with lms.Client() as client:
        model = client.llm.model("qwen3-14b", config={"contextLength": 10240})
        result = model.respond(prompt)
    return result


def write_csv(generation_prompt:list[str], prompt:list[str],response:list[str], output:str):
    header = ["generation_prompt", "prompt", "response"]
    with open(output,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(zip(generation_prompt, prompt, response))
    print("Wrote file")

def main():
    question = read_csv("./brainstorming/brainstorming-2k.csv")
    generation_prompt = create_prompt(question)
    llm_response = generate_thinking(generation_prompt)
    write_csv(generation_prompt, question, llm_response, "./brainstorming/brainstorming-thinking.csv")

if __name__ == "__main__":
    main()
