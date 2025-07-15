import json
import os

def extract_question_ids(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {filepath}: {e}")
            return set()

    question_ids = set()
    
    def recurse(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'questionIdentifier':
                    question_ids.add(str(value))  # Convert to string to normalize
                else:
                    recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)

    recurse(data)
    return question_ids

# 🔁 Update these with your file paths
file1_path = r'C:\path\to\file1.json'
file2_path = r'C:\path\to\file2.json'

if os.path.exists(file1_path) and os.path.exists(file2_path):
    ids1 = extract_question_ids(file1_path)
    ids2 = extract_question_ids(file2_path)

    print("✅ Common questionIdentifiers:")
    print(sorted(ids1 & ids2))

    print("\n❌ Present only in file1:")
    print(sorted(ids1 - ids2))

    print("\n❌ Present only in file2:")
    print(sorted(ids2 - ids1))
else:
    print("❗One or both files do not exist. Please check the file paths.")