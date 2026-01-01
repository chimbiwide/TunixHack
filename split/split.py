import csv
import random

def databricks(file:str = "./Databricks/databricks-reasoning.csv") -> dict:
    open_qa = []
    general_qa = []
    classification = []
    closed_qa = []
    brainstorming = []
    information_extraction = []
    summarization = []
    creative_writing = []

    categories = {
        "open_qa": open_qa,
        "general_qa": general_qa,
        "classification": classification,
        "closed_qa": closed_qa,
        "brainstorming": brainstorming,
        "information_extraction": information_extraction,
        "summarization": summarization,
        "creative_writing": creative_writing
    }
    with open (file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line = [row.get("prompt"), row.get("model-response")]

            category = row.get("categories")
            if category in categories:
                categories[category].append(line)
    return categories

def CreativeWriting(file:str = "./CreativeWriting/writing-thinking.csv") -> list:
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line = [row.get("prompt"), row.get("response")]
            data.append(line)
    return data

def SciQA(file:str = "./SciQA/sciqa-thinking.csv") -> list:
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line = [row.get("prompt"), row.get("response")]
            data.append(line)
    return data

def brainstorming(file:str = "./brainstorming/brainstorming-thinking.csv") -> list:
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line = [row.get("prompt"), row.get("response")]
            data.append(line)
    return data

def code(file:str = "./code/code-thinking.csv") -> list:
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line = [row.get("prompt"), row.get("response")]
            data.append(line)
    return data

def gsm8k(file:str = "./gsm8k/gsm8k-thinking.csv") -> list:
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line = [row.get("question"), row.get("answer")]
            data.append(line)
    return data

# the 1.5k rows of general qa question
def random_qa(databricks:dict) -> list:
    return (random.sample(databricks["open_qa"], 500) + random.sample(databricks["general_qa"], 500) + random.sample(databricks["closed_qa"], 500))

# keep all coding problems since there is only 427 rows anyways

# the 1k rows of SciQA
def random_sci(SciQA:list) -> list:
    return (random.sample(SciQA, 1000))

# the 1k rows of gsm8k
def random_gsm(gsm:list) -> list:
    return (random.sample(gsm, 1000))

# the 2.5k rows of creative writing
def random_writing(databricks:dict, CreativeWriting:list) -> list:
    return (databricks["creative_writing"] + random.sample(CreativeWriting, 1891))

# the 2k rows of brainstorming
def random_brainstorming(databricks:dict, brainstorming:list) -> list:
    return (random.sample(databricks["brainstorming"], 1000) + random.sample(brainstorming, 1000))

# keep all summarization question 1188 rows
def get_summarization(databricks:dict) -> list:
    return databricks["summarization"]

# 250 rows from information_extraction
def random_info(databricks:dict) -> list:
    return random.sample(databricks["information_extraction"], 250)

# the 250 rows from classification
def random_class(databricks:dict) -> list:
    return random.sample(databricks["classification"], 250)

def write_csv(data:list, output:str) -> None:
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["prompt", "response", "category"])
        writer.writerows(data)

def split_sft_rl(data:list, sft_ratio: float = 0.2) -> tuple[list, list]:
    shuffled_data = data.copy()
    random.shuffle(shuffled_data)

    split_loc = int(len(shuffled_data) * sft_ratio)
    sft_data = shuffled_data[:split_loc]
    rl_data = shuffled_data[split_loc:]

    return sft_data, rl_data

def add_category(data:list, category: str) -> list:
    return [row + [category] for row in data]

def main():
    brick = databricks()
    writing = CreativeWriting()
    science = SciQA()
    brain = brainstorming()
    vibe_code = code()
    math = gsm8k()

    general_qa = add_category(random_qa(brick), "general_qa")
    code_data = add_category(vibe_code, "code")
    sci_qa = add_category(random_sci(science), "science_qa")
    gsm = add_category(random_gsm(math), "math")
    creative_writing = add_category(random_writing(brick, writing), "creative_writing")
    brainstorm = add_category(random_brainstorming(brick, brain), "brainstorming")
    summarization = add_category(get_summarization(brick), "summarization")
    info = add_category(random_info(brick), "information_extraction")
    classification = add_category(random_class(brick), "classification")

    #split the dataset into SFT and RL
    categories = [
        general_qa,
        code_data,
        sci_qa,
        gsm,
        creative_writing,
        brainstorm,
        summarization,
        info,
        classification
    ]
    all_sft = []
    all_rl = []

    for category_data in categories:
        sft,rl = split_sft_rl(category_data)
        all_sft.extend(sft)
        all_rl.extend(rl)

    data = general_qa + code_data + sci_qa + gsm + creative_writing + brainstorm + summarization + info + classification

    write_csv(data, "./split/think-10k.csv")
    write_csv(all_sft, "./split/sft2k-think.csv")
    write_csv(all_rl, "./split/rl8k-think.csv")

if __name__=="__main__":
    main()
