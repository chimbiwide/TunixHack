# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

reasoning_start = "<reasoning>"
reasoning_end = "</reasoning>"
solution_start = "<answer>"
solution_end = "</answer>"

# SYSTEM_PROMPT = f"""You are given a problem. First, think about the problem \
# and provide your reasoning. Place it between {reasoning_start} and \
# {reasoning_end}. Then, provide the final answer between {solution_start} and {solution_end}."""

question = "Our e-commerce website has been receiving negative feedback from customers regarding shipping times and product quality. What can we do to improve customer satisfaction? What are some ways to improve customer satisfaction for our e-commerce website?" 

tokenizer = AutoTokenizer.from_pretrained("KeeganC/gemma-3-1b-it-thinking")
model = AutoModelForCausalLM.from_pretrained("KeeganC/gemma-3-1b-it-thinking")
messages = [
    {"role": "user", "content": f"""
         Problem: {question}
    """},
]
inputs = tokenizer.apply_chat_template(
	messages,
	add_generation_prompt=True,
	tokenize=True,
	return_dict=True,
	return_tensors="pt",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=512)
print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]))
