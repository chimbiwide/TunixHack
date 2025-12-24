#dont need context
creative_writing = """
You will be given a creative writing prompt. Generate the reasoning traces that get to the final response.
Your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
"""
# need context
closed_qa = """
You will be given a question, and a passage of relevant information. Generate the reasoning traces that get to the final answer.
Your reasoning should logically lead to your final answer, think about how you will structure the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
"""
# need context
open_qa = """
You will be given a question, and a correct answer. Generate the reasoning traces that get to the final answer.
Your reasoning should logically lead to your final answer, think about how you will structure the reasoning traces.
Do not reference that the correct answer was provided in the reasoning traces.
You can paraphrase the answer and add additional information.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>

"""
# need context
summarization = """
You will be given a question, and a paragraph you must summarize the answer from.
Generate the reasoning traces that get to the final answer.
Your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>

"""
# need context
information_extraction = """
You will be given a question, and a supplementary text. Your answer should be based on the text provided.
Generate the reasoning traces that get to the final answer.
Your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>

"""

#need context
classification = """
You will be given a classification question and the correct answer. Generate the reasoning traces that get to the final answer.
Your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
Do not reference that the correct answer was provided in the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>

"""

#dont need context
brainstorming = """
You will be given a brainstorming idea. Generate the reasoning traces that get to the final answer.
your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
your final final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>

"""

#dont need context
general_qa = """
You will be given a open-ended question. Generate the reasoning traces that get to the final answer.
your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
your final final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>

"""

# Dictionary mapping category names to prompts
PROMPTS = {
    "creative_writing": creative_writing,
    "closed_qa": closed_qa,
    "open_qa": open_qa,
    "summarization": summarization,
    "information_extraction": information_extraction,
    "classification": classification,
    "brainstorming": brainstorming,
    "general_qa": general_qa,
}
