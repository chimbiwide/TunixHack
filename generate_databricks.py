import lmstudio as lms
import json

def process_file(filename: str):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            line.strip()
            currectLine = json.loads(line)
            system_prompt =

def create_system_prompt(currentLine):
    prompt = currentLine.get("instruction")
    context = currentLine.get("context")
    response = currentLine.get("response")
    category = currentLine.get("category")

    System_prompt_template = f"""
    
    """