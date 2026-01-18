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

def cnn_summarization(file:str = "./summarization/summarization-thinking.csv") -> list:
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line = [row.get("prompt"), row.get("response")]
            data.append(line)
    return data

# ===== 21K Dataset Functions =====
# These functions create the 21k dataset with specific row counts per category

# 3k rows of general qa (from open_qa + general_qa + closed_qa)
def get_21k_qa(databricks:dict) -> list:
    all_qa = databricks["open_qa"] + databricks["general_qa"] + databricks["closed_qa"]
    return random.sample(all_qa, min(3000, len(all_qa)))

# All code rows (11,280 rows available, user mentioned 427 but we'll use all)
def get_21k_code(code:list) -> list:
    return code  # Use all available code rows

# 2k rows from SciQA
def get_21k_science(SciQA:list) -> list:
    return random.sample(SciQA, min(2000, len(SciQA)))

# 2k rows from gsm8k
def get_21k_math(gsm:list) -> list:
    return random.sample(gsm, min(2000, len(gsm)))

# 5.7k rows of creative writing (all databricks creative_writing + remainder from CreativeWriting)
def get_21k_writing(databricks:dict, CreativeWriting:list) -> list:
    target = 5700
    databricks_creative = databricks["creative_writing"]  # 709 rows
    remaining_needed = target - len(databricks_creative)

    if remaining_needed > 0 and len(CreativeWriting) > 0:
        sample_size = min(remaining_needed, len(CreativeWriting))
        return databricks_creative + random.sample(CreativeWriting, sample_size)
    else:
        return databricks_creative

# 3k rows of brainstorming (combination of databricks + standalone)
def get_21k_brainstorming(databricks:dict, brainstorming:list) -> list:
    target = 4000
    databricks_brain = databricks["brainstorming"]  # 1,766 rows
    remaining_needed = target - len(databricks_brain)

    if remaining_needed > 0 and len(brainstorming) > 0:
        sample_size = min(remaining_needed, len(brainstorming))
        return databricks_brain + random.sample(brainstorming, sample_size)
    else:
        return databricks_brain[:target]

# 2,188 rows of summarization (databricks + cnn)
def get_21k_summarization(databricks:dict, cnn:list) -> list:
    target = 2188
    databricks_summ = databricks["summarization"]  # 1,188 rows
    remaining_needed = target - len(databricks_summ)

    if remaining_needed > 0 and len(cnn) > 0:
        sample_size = min(remaining_needed, len(cnn))
        return databricks_summ + random.sample(cnn, sample_size)
    else:
        return databricks_summ

# 1k rows from information_extraction
def get_21k_info(databricks:dict) -> list:
    return random.sample(databricks["information_extraction"], min(1000, len(databricks["information_extraction"])))

# 1k rows from classification
def get_21k_class(databricks:dict) -> list:
    return random.sample(databricks["classification"], min(1000, len(databricks["classification"])))


# ===== Legacy Functions (kept for backwards compatibility) =====

# the 1.5k rows of general qa question
def random_qa(databricks:dict) -> list:
    return (random.sample(databricks["open_qa"], 500) + random.sample(databricks["general_qa"], 500) + random.sample(databricks["closed_qa"], 500))

def get_qa(databricks: dict) -> list:
    return (databricks["open_qa"] + databricks["general_qa"] + databricks["closed_qa"])

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

def get_writing(databricks:dict, CreativeWriting:list) -> list:
    return (databricks["creative_writing"] + CreativeWriting)

# the 2k rows of brainstorming
def random_brainstorming(databricks:dict, brainstorming:list) -> list:
    return (random.sample(databricks["brainstorming"], 1000) + random.sample(brainstorming, 1000))

def get_brainstorming(databricks:dict, brainstorming:list) -> list:
    return (databricks["brainstorming"] + brainstorming)

# keep all summarization question 1188 rows
def get_summarization(databricks:dict, cnn:list) -> list:
    return (databricks["summarization"] + cnn)

# 250 rows from information_extraction
def random_info(databricks:dict) -> list:
    return random.sample(databricks["information_extraction"], 250)

def get_info(databricks:dict) -> list:
    return databricks["information_extraction"]

# the 250 rows from classification
def random_class(databricks:dict) -> list:
    return random.sample(databricks["classification"], 250)

def get_class(databricks:dict) -> list:
    return databricks["classification"]

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
    cnn = cnn_summarization()

    general_qa = add_category(get_21k_qa(brick), "general_qa")
    code_data = add_category(vibe_code, "code")
    sci_qa = add_category(get_21k_science(science), "science_qa")
    gsm = add_category(get_21k_math(math), "math")
    creative_writing = add_category(get_writing(brick, writing), "creative_writing")
    brainstorm = add_category(get_21k_brainstorming(brick, brain), "brainstorming")
    summarization = add_category(get_21k_summarization(brick, cnn), "summarization")
    info = add_category(get_21k_info(brick), "information_extraction")
    classification = add_category(get_21k_class(brick), "classification")

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

    write_csv(data, "./split/think.csv")
    write_csv(all_sft, "./split/sft-think.csv")
    write_csv(all_rl, "./split/rl-think.csv")

if __name__=="__main__":
    main()
