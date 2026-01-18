import csv
from collections import Counter

def count_categories(csv_file):
    """Read CSV and count rows per category"""
    category_counts = Counter()

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row['category']
            category_counts[category] += 1

    return category_counts

def main():
    csv_file = 'think.csv'

    # Count categories
    counts = count_categories(csv_file)

    # Print results
    print("Category counts in think.csv:")
    print("-" * 50)

    total = 0
    for category, count in sorted(counts.items()):
        print(f"{category:<30} {count:>10,}")
        total += count

    print("-" * 50)
    print(f"{'TOTAL':<30} {total:>10,}")

if __name__ == "__main__":
    main()
