import sqlite3

conn = sqlite3.connect('instance/social_engineering_awareness.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Available tables:')
for table in tables:
    print(f'- {table[0]}')

print('\n' + '='*50)

# Check for question-related tables
question_tables = [t[0] for t in tables if 'question' in t[0].lower()]
print(f'Question-related tables: {question_tables}')

# Check each question table for Module 2 questions
for table in question_tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE module_id = 2")
        count = cursor.fetchone()[0]
        print(f'Module 2 questions in {table}: {count}')
        
        if count > 0:
            cursor.execute(f"SELECT id, question_text FROM {table} WHERE module_id = 2 LIMIT 2")
            questions = cursor.fetchall()
            for q in questions:
                print(f'  ID: {q[0]}, Question: {q[1][:50]}...')
    except Exception as e:
        print(f'Error checking {table}: {e}')

conn.close()
