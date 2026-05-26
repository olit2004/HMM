import csv

dataset_path = 'archive/brown.csv'

try:
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print("Header:")
        print(header)
        print("\nFirst 5 rows:")
        for i in range(5):
            try:
                row = next(reader)
                print(f"Row {i+1}:")
                print(row)
                print("-" * 40)
            except StopIteration:
                break
except Exception as e:
    print(f"Error reading dataset: {e}")
