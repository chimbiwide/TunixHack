import lmstudio as lms
import re
model = lms.llm()
def replace_thinking(response:str):
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
print(replace_thinking(model.respond("Who are you").content).strip())