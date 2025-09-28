import json

with open('content_seed/modules.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find Module 2
module2 = None
for module in data['modules']:
    if module['order'] == 2:
        module2 = module
        break

if module2:
    print(f'Module 2 found: {module2["name"]}')
    print(f'Has questions: {"questions" in module2}')
    if 'questions' in module2:
        print(f'Number of questions: {len(module2["questions"])}')
        if len(module2['questions']) > 0:
            print(f'First question: {module2["questions"][0]["question_text"][:50]}...')
            print(f'Question set: {module2["questions"][0].get("question_set", "not set")}')
    else:
        print('No questions found in Module 2')
else:
    print('Module 2 not found')
