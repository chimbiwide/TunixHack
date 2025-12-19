import csv
import json

def create_prompt(filename:str):
    prompts = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            str = json.loads(line)
            prompt_txt = str["instruction"]

            if str["context"]:
                match str["category"]:
                    case "summarization":
                        prompt_txt += "\nContext: " + str["context"]
                    case "closed_qa":
                        prompt_txt += "\nContext: " + str["context"]
                    case "information_extraction":
                        prompt_txt += "\nSupplementary Text: " + str["context"]
            prompts.append(prompt_txt)

    return prompts

def read_csv(filename: str):
    categories = []
    generation_prompt = []
    model_response = []

    with open(filename, 'r')  as f:
        reader = csv.DictReader(f)
        for row in reader:
            categories.append(row["Categories"])
            generation_prompt.append(row["Generation Prompt"])
            model_response.append(row["Model_Response"])

    return categories, generation_prompt, model_response

def write_csv(gen_prompt:list[str], prompt:list[str], model_response:list[str], categories:list[str], output:str):
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ["generation-prompt", "prompt", "model-response", "categories"]
        writer.writerow(header)
        writer.writerows(zip(gen_prompt, prompt, model_response, categories))
    print("wrote file")

def main():
    prompts = create_prompt("databricks.jsonl")
    categories, gen_prompt, model_response = read_csv("databricks_with_reason.csv")
    write_csv(gen_prompt, prompts, model_response, categories, "fixed_databricks.csv")

if __name__ == "__main__":
    main()


