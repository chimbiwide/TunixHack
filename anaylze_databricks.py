import csv

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

def write_csv(categories: dict, output:str):
    fieldnames = ['open_qa', 
                  'general_qa', 
                  'classification',
                  'closed_qa',
                  'brainstorming',
                  'infomation_extraction',
                  'summarization',
                  'creative_writing'
                  ]
    with open (output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(categories)
        print("wrote_file")

def main():
    cat_count = count_categories("databricks_with_reason.csv")
    print(cat_count)
    #write_csv(cat_count, "categories_count.csv")

if __name__ == "__main__":
    main()
