from openai import OpenAI
from dotenv import load_dotenv
import os

from chat_adapter import ChatAdapter
from tools.tools import save_response_to_file

# === KONFIGURACJA ===
MODEL_NAME = "gpt-4-turbo"
SAVE_FILE_PATH = ""
load_dotenv()
# === INICJALIZACJA KLIENTA OPENAI ===
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === FUNKCJA GŁÓWNA ZAPYTAŃ ===
def chat_with_openai(system_prompt, user_input):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    return response.choices[0].message.content

# === FORMATOWANIE ODPOWIEDZI ===
def format_response(response):
    lines = response.strip().split('\n')
    formatted = "\n".join(f"{line}" for line in lines)
    return formatted



# === TEMPLATE DODATKOWEGO NARZĘDZIA ===
def my_tool(data):
    # Miejsce na dodatkowe narzędzia
    print("[MyTool] Narzędzie jeszcze niezaimplementowane.")

# === FUNKCJA GŁÓWNA ===
def main():
    chat_adapter = ChatAdapter()

    print("=== Starting OpenAI chat... ===")
    system_prompt = """
    Ładnie się przywitaj i powiedz, że potrzebujesz pomocy.".
    """
    try:
            agent_response = chat_with_openai(system_prompt, "Testowe polecenie poczatkowe")
            agent_response_formatted = format_response(agent_response)
            print("\nAI:\n" + agent_response_formatted)
            mbank_answer=chat_adapter.send_message(agent_response_formatted)
            print("\nmBank:\n" + str(mbank_answer))
            save_response_to_file(agent_response_formatted, mbank_answer)
    except Exception as e:
            print(f"Error: {e}")



# === URUCHOMIENIE ===
if __name__ == "__main__":
    main()
