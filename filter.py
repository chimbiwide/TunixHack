import csv
import sys
from pathlib import Path


def read_csv(file_path: str) -> list:
    """Read CSV file and return list of rows"""
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Read header
        rows.append(header)
        for row in reader:
            rows.append(row)
    return rows


def combine_and_deduplicate(file1: str, file2: str, output: str):
    """Combine two CSV files and remove duplicate rows"""
    # Read both files
    print(f"Reading {file1}...")
    rows1 = read_csv(file1)
    header = rows1[0]
    data1 = rows1[1:]

    print(f"Reading {file2}...")
    rows2 = read_csv(file2)
    data2 = rows2[1:]  # Skip header from second file

    # Combine data
    combined = data1 + data2
    print(f"Combined {len(data1)} + {len(data2)} = {len(combined)} rows")

    # Remove duplicates while preserving order
    seen = set()
    unique_rows = []

    for row in combined:
        # Convert row to tuple for hashing
        row_tuple = tuple(row)
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_rows.append(row)

    print(f"Removed {len(combined) - len(unique_rows)} duplicate rows")
    print(f"Final dataset: {len(unique_rows)} unique rows")

    # Write output
    write_csv(unique_rows, header, output)
    print(f"Written to {output}")


def write_csv(data: list, header: list, output: str):
    """Write data to CSV file"""
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python filter.py <input_file1.csv> <input_file2.csv> <output_file.csv>")
        print("\nExample:")
        print("  python filter.py data1.csv data2.csv combined_clean.csv")
        sys.exit(1)

    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]
    output_file = sys.argv[3]

    # Validate input files exist
    if not Path(input_file1).exists():
        print(f"Error: {input_file1} does not exist")
        sys.exit(1)

    if not Path(input_file2).exists():
        print(f"Error: {input_file2} does not exist")
        sys.exit(1)

    combine_and_deduplicate(input_file1, input_file2, output_file)
