import re
import lmstudio as lms

def replace_thinking(response:str):
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()

def llm_instance(prompt:str):
    with lms.Client() as client:
        model = client.llm.model("qwen3-14b")
        chat = lms.Chat()
        chat.add_user_message(prompt)
        result = model.respond(chat)
    return result
