import csv
import lmstudio as lms
import re

PROMPT = """
You will be given a general science question along with the correct answer and a paragraph of supporting text.
Generate the reasoning traces that get to the final correct answer.
Your reasoning should logically lead to the final answer, think about how you will structure the reasoning traces.
Do not reference that the correct answer is provided in the reasoning traces.
Treat the supporting text as your own knowledge, do not explicitly reference that your are provided with a paragraph of supporting text.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
"""

def read_csv(filename:str):
    question = []
    answer = []
    support_text = []

    with open(filename, 'r') as f:
        file = csv.DictReader(f)

        for line in file:
            question.append(line.get("question"))
            answer.append(line.get("correct_answer"))
            support_text.append(line.get("support"))
    return question, answer, support_text

def create_prompt(q:list[str],a:list[str],t:list[str]) -> list[str]:
    prompts = []
    for question, answer, support in zip(q,a,t):
        prompt = f"{PROMPT}\nQuestion: {question}\nCorrect Answer: {answer}\nSupporting Text: {support}" 
        prompts.append(prompt)
    return prompts

def replace_thinking(response:str):
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()

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


def write_csv(generation_prompt:list[str], prompt:list[str],response:list[str], output:str):
    header = ["generation_prompt", "prompt", "response"]
    with open(output,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(zip(generation_prompt, prompt, response))
    print("Wrote file")

def main():
    question, answer, support = read_csv("./SciQA/sciqa-3k.csv")
    generation_prompt = create_prompt(question, answer, support)
    llm_response = generate_thinking(generation_prompt)
    write_csv(generation_prompt, question, llm_response, "./SciQA/sciqa-thinking.csv")

if __name__ == "__main__":
    main()
