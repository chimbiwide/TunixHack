creative_writing = """
You will be given a creative writing prompt. Generate the reasoning traces that get to the final response. 
Your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
"""

closed_qa = """
You will be given a question, and a passage of relevant information. Generate the reasoning traces that get to the final answer.
Your reasoning should logically lead to your final answer, think about how you will structure the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
"""

open_qa = """
You will be given a question, and a correct answer. Generate the reasoning traces that get to the final answer.
Your reasoning should logically lead to your final answer, think about how you will structure the reasoning traces.
Do not reference that the correct answer was provided in the reasoning traces.
You can paraphrase the answer and add additional information.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
"""

summarization = """
You will be given a question, and a paragraph you must summarize the answer from.
Generate the reasoning traces that get to the final answer.
Your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
"""