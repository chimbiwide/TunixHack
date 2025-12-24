import csv

def read_csv(input:str):
    question = []
    answer = []
    with open(input, 'r') as f:
        file = csv.DictReader(f)
        for line in file:
            question.append(line.get("question"))
            
            solution = line.get("answer")
            answer.append(process_answer(solution))
    return question, answer

def process_answer(answer:str) -> str:
    answer = answer.replace("#### ", "</reasoning><answer>", 1)
    return f"<reasoning>{answer}</answer>"

def write(Q:list[str],A:list[str],output:str) -> None:
    header = ["question", "answer"]
    with open(output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(zip(Q,A))
    print("Wrote file")

def main():
    question, answer = read_csv("./gsm8k/gsm8k.csv")
    write(question, answer, "./gsm8k/gsm8k-thinking.csv")

if __name__ == "__main__":
    main()
