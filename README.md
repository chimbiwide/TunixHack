# databricks-thinking

Created by extracing the questions from the [databricks-dolly] dataset and using Qwen3-14b to synthetically generate reasoning traces and answers.

The whole process took 1 day 23 hours 18 minuntes and 8 seconds

---

### Why we created this dataset
The vast majority of publicly available datasets comes from large models such as DeepSeek R1.

The issue with using these large models are obvious: the reasoning traces are extremely long, often longer than the actual answer.

As point out by the paper [Small Models Struggle to Learn from Strong Reasoners], smaller models such as Gemma3-1B struggle learning from long CoT reasoning, performing better when the reasoning traces are shorter.

The second problem is that most of the reasoning datasets are focused on Math, coding and science, with little to no attention paid to creative tasks such as writing, brainstorming or summarization.

As a group more interested in enhancing the roleplaying capabilities of smaller models (check out our previous work!), we wanted to focus more on the creative aspect of LLMs.

So, that is why we picked the `databricks-dolly` dataset, as it's a human-curated dataset that consists of mostly creative tasks and qa questions that are more open ended.

---

### Why Qwen3-14b?

The other question we struggle with is which model to pick to generate the reasoning traces, as we can't really use humans...

We have a 5070TI, which allowed us to run some decent models locally, so we mostly focused on local models
We created a list of models that we tested (all with thinking turned on)

- DeepSeekR1 API (of course)
- Gemini 2.0 Flash
- one of the DeepSeek distilled models
- Qwen 3 series (4B-thinking-2507, 14b, 30B-thinking-2507)

So we randomly took 20 questions from databricks and used this prompt(we did use different prompts for tasks such as summarization and brainstorming):
```
You will be given a question, and a passage of relevant information. Generate the reasoning traces that get to the final answer.
Your reasoning should logically lead to your final answer, think about how you will structure the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
```

Despite the API pricing for DeepSeek and Gemini 2.0 being relatively cheap, running it on a 15k dataset is still a little too expensive.

Out of all the local models we tested, Qwen3-14B won as it can generate short reasoning traces without the need for a specific prompt, runs fast enough on our GPU (60 tps) and has enough knowledge to actually answer the question (4B stuggled at this).

---

Couple of osoning traces without the need for a specific prompt, runs fast enough on our GPU (60 tps) and has enough knowledge to actually answer the question (4B stuggled at this).

---

### Couple of observations

1. As we mentioned before, Qwen3-14b produces short concise reasoning traces with minimum prompting.
2. Good instruction following, for each question Qwen typically thinks for about 10 seconds before answering, and it can always follow the given answer format.
3. Good reasoning traces, the generated reasoning traces are surprisingly short and logical.


---

### Example Answer

Here is an example of our prompt and the Qwen's answer

Question
```
You will be given a creative writing prompt. Generate the reasoning traces that get to the final response. 
Your reasoning should logically lead to your final response, think about how you will structure the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>

Prompt: write a scene between two actors discussing movie Inception
```

Answer:
```
<reasoning>
To create a realistic and engaging scene between two actors discussing *Inception*, I first consider their likely relationship and setting. A casual café meeting allows for relaxed conversation. Next, I identify key themes from the film: dreams vs. reality, emotional stakes (Cobb’s guilt), and the layered plot structure. The dialogue should reflect their familiarity with the movie, incorporating specific terms like "kick" or "totem." One actor could analyze the narrative complexity, while the other focuses on emotional resonance, creating a dynamic exchange. Including references to iconic scenes (e.g., zero-gravity fight) adds authenticity. Finally, the conversation concludes with mutual appreciation of the film’s impact, ensuring natural flow and avoiding technical jargon overload.
</reasoning>
<answer>
**Scene: Two actors, Maya and Jordan, sit across from each other at a cozy café. The hum of espresso machines blends with their voices.**

**Maya:** (sipping her latte) I still can’t wrap my head around the ending. You think Cobb *actually* fell asleep on that beach? Or was it another layer?

**Jordan:** (leaning forward) That’s the genius, right? Nolan leaves it ambiguous. The spinning top never stops—maybe he’s trapped in a loop of guilt, or maybe he finally lets go. Either way, it’s a mirror for the audience. We’re all questioning reality by the time the credits roll.

**Maya:** (nodding) But what about the emotional core? Cobb’s whole journey isn’t just about inception—it’s about reconciling with Mal. That scene where he confronts her in the dream… It’s haunting. How do you play that without making it melodramatic?

**Jordan:** (pausing) You lean into the vulnerability. The weight of his choices. When he says, “I’m not dreaming,” it’s not just a line—it’s him fighting to hold onto truth. The film’s a paradox: it’s about planting ideas, but the real inception is making us question our own perceptions.

**Maya:** (smiling) And the action? That zero-gravity fight scene… How do you even *visualize* that as an actor?

**Jordan:** (grinning) You trust the director. Nolan’s like a magician—pulls you into worlds where physics bend, but the emotions stay grounded. It’s why the movie sticks. You leave thinking about dreams, but also about what you’re willing to let go of.

**Maya:** (raising her cup) To inception, then. The best kind of chaos.

**Jordan:** (clinking his mug) And the best kind of art.

*(They both laugh as the barista calls out an order, pulling them back to reality.)*
</answer>
```
