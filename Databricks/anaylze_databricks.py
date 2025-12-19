import csv
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("unsloth/gemma-3-1b-it")

def count_categories(filename:str):
    categories = {
            "open_qa": 0,
            "general_qa" :0,
            "classification" : 0,
            "closed_qa" : 0,
            "brainstorming" : 0,
            "information_extraction" : 0,
            "summarization" : 0,
            "creative_writing":0
    }
    with open(filename, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            categories[row["Categories"]] += 1

    return categories

def count_tokens(txt:str) -> int:
    return len(tokenizer.encode(txt))

def in_limit(txt:str, max_tokens:int=1024) -> bool:
    return count_tokens(txt) <= max_tokens


def filter_csv(input:str, output:str, max_tokens:int=1024):
    with open(input, 'r') as in_f, open(output, 'w', newline='') as out_f:
        reader = csv.DictReader(in_f)
        writer  = csv.DictWriter(out_f,fieldnames=reader.fieldnames)
        writer.writeheader()

        total = 0
        kept = 0

        for row in reader:
            total += 1
            
            target_text = row["Prompt"] + row["Model_Response"]
            
            if in_limit(target_text, max_tokens=max_tokens):
                writer.writerow(row)
                kept += 1

        print(f"Kept {kept}/{total} conversations")


def write_categories(categories: dict, output:str):
    fieldnames = ['open_qa', 
                  'general_qa', 
                  'classification',
                  'closed_qa',
                  'brainstorming',
                  'information_extraction',
                  'summarization',
                  'creative_writing'
                  ]
    with open (output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow(categories)
        print("wrote_file")


def main():
    cat_count = count_categories("databricks_with_reason.csv")
    print(cat_count)
    write_categories(cat_count, "categories_count.csv")

if __name__ == "__main__":
    print(count_tokens("""

    """))
