with open('scratch/batch_08.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"rule_type": "prerequisite"', '"rule_type": "clinical_prerequisite"')

with open('scratch/batch_08.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed batch_08.py rule_type enum values.")
