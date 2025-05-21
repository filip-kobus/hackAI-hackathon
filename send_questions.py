import json
import requests

def load_questions(file_path):
    """Load questions from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [entry["question"] for entry in data]

def send_question(api_url, question):
    """Send a question to the API and return the response."""
    try:
        response = requests.post(api_url, json={"message": question})
        response.raise_for_status()
        return response.json().get("response", "No response from API")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def append_to_results_file(results_file, question, response):
    """Append a question-answer pair to the results JSON file."""
    try:
        try:
            with open(results_file, 'r', encoding='utf-8') as file:
                results = json.load(file)
        except FileNotFoundError:
            results = []

        results.append({"question": question, "answer": response})

        with open(results_file, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving results: {e}")

def main():
    questions_file = "./data/questions_answers-v1.json" 
    results_file = "./data/results.json"
    api_url = "http://127.0.0.1:8000/send_message"

    questions = load_questions(questions_file)

    print("Starting to send questions...")

    for idx, question in enumerate(questions, start=1):
        print(f"Question {idx}: {question}")
        response = send_question(api_url, question)
        print(f"Response: {response}\n")

        append_to_results_file(results_file, question, response)

if __name__ == "__main__":
    main()
