import re
import json
import os

questions_path = os.path.abspath(r'C:\Users\filip\OneDrive\Dokumenty\HackAI\data\mbank-pytania-v1.md')

def extract_questions_and_answers(filename):
    questions_and_answers = []
    current_question = None
    current_answer = []

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^(###)\s+(.*)', line)
            if match:
                if current_question:
                    questions_and_answers.append({
                        "question": current_question,
                        "answer": "\n".join(current_answer).strip()
                    })
                current_question = match.group(2).strip()
                current_answer = []
            elif current_question:
                current_answer.append(line.strip())

        if current_question:
            questions_and_answers.append({
                "question": current_question,
                "answer": "\n".join(current_answer).strip()
            })

    return questions_and_answers

if __name__ == "__main__":
    questions_and_answers = extract_questions_and_answers(questions_path)
    with open('questions_answers.json', 'w', encoding='utf-8') as f:
        json.dump(questions_and_answers, f, ensure_ascii=False, indent=2)
    for qa in questions_and_answers:
        print(f"Question: {qa['question']}")
        print(f"Answer: {qa['answer']}\n")