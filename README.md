Checklist:

- [x] [creative essay prompt](https://huggingface.co/datasets/sam-paech/essays-creative-writing-prompts)
- [x] [Basic Science QA](https://huggingface.co/datasets/allenai/sciq)
- [ ] [Brainstorming](https://huggingface.co/datasets/Wanfq/Explore_Instruct_Brainstorming_10k)
- [x] [Math](https://huggingface.co/datasets/openai/gsm8k)
- [ ] [Rewriting](https://huggingface.co/datasets/Wanfq/Explore_Instruct_Rewriting_10k/viewer/default/train?views%5B%5D=train&row=14)
- [ ] [Code](https://huggingface.co/datasets/Muennighoff/mbpp)

# TunixHack

Code for [chimbiwide](https://huggingface.co/chimbiwide) and [KeeganC](https://huggingface.co/KeeganC)'s [Google Tunix Hack](https://www.kaggle.com/competitions/google-tunix-hackathon/overview) hackathon submission.

---

### Introduction(-ish)

The goal is to use Google's new TPU based post-training library Tunix to teach Gemma3-1b to reason, not a new thing, but its a new library. 

As specified in the hackathon page, it's less focused on code and mathematics. So we put a bigger emphasis in creative writing and brainstorming (creative ideation).

The collection of datasets can be found on [HuggingFace](https://huggingface.co/collections/npcLM/reasoning-datasets)

---

### Structure

```
  TunixHack/
  ├── brainstorming/            
  │   └── generate.py
  ├── code/                       
  │   └── generate.py
  ├── crap.py                     // Shared utilities (tried to use that, but copying and pasting is easier)
  ├── CreativeWriting/           
  │   ├── generate.py
  │   ├── prompts.py
  ├── Databricks/                 
  │   ├── anaylze_databricks.py
  │   ├── generate_databricks.py
  │   ├── rework_databricks.py
  │   └── test.py
  ├── gsm8k/                      
  │   ├── generate.py
  ├── pyproject.toml      
  ├── README.md
  ├── SciQA/                  
  │   ├── generate.py
```

Each folder corresponds to one dataset, and it always has the `generate.py` script, which uses the LM Studio SDK to inference Qwen3-14b to generate the reasoning traces.

---

### Why Qwen3-14b?

The other question we struggle with is which model to pick to generate the reasoning traces, as we can't really use humans...

We have a 5070TI, which allowed us to run some decent models locally, so we mostly focused on local models
We created a list of models that we tested (all with thinking turned on)

- DeepSeekR1 API (of course)
- Gemini 2.0 Flash
- Qwen 3 series (4B-thinking-2507, 14b, 30B-thinking-2507)

So we extracted about 100 prompts from all the datasets combined and prompted the models listed above.

Despite the API pricing for DeepSeek and Gemini 2.0 being relatively cheap, using them on 24k rows is still too expensive.

Out of all the local models we tested, Qwen3-14B won as it can generate short reasoning traces without the need for a specific prompt, runs fast enough on our GPU (60 tps) and has enough knowledge to actually answer the question (4B stuggled at this).
