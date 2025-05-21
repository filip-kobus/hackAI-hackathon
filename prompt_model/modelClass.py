import os
import requests

from chat_adapter import ChatAdapter
from ai_agent import LlamaChat
from tools.tools import save_response_to_file

# === KONFIGURACJA ===
MODEL_NAME = "llama3"
OLLAMA_API_URL = "http://172.27.27.79:11434/api/chat"
SAVE_FILE_PATH = ""

# === FORMATOWANIE ODPOWIEDZI ===
def format_response(response):
    lines = response.strip().split('\n')
    formatted = "\n".join(f"{line}" for line in lines)
    return formatted

# === TEMPLATE DODATKOWEGO NARZĘDZIA ===
def my_tool(data):
    print("[MyTool] Narzędzie jeszcze niezaimplementowane.")

# === FUNKCJA GŁÓWNA ===
def main():
    chat_adapter = ChatAdapter()
    agent = LlamaChat(MODEL_NAME, OLLAMA_API_URL)
    print("=== Starting LLaMA 3 chat (via Ollama)... ===")
    system_prompt = """
    Ładnie się przywitaj i powiedz, że potrzebujesz pomocy. Rozmawiasz z chatbotem, który jest w stanie odpowiadać na pytania dotyczące bankowości, finansów i produktów oferowanych przez mBank.
    """

    try:
        agent_response = agent.send_prompt(system_prompt, "Testowe polecenie początkowe")
        agent_response_formatted = format_response(agent_response)
        print("\nAI:\n" + agent_response_formatted)

        mbank_answer = chat_adapter.send_message(agent_response_formatted)
        print("\nmBank:\n" + str(mbank_answer))

        save_response_to_file(agent_response_formatted, mbank_answer)

    except Exception as e:
        print(f"Error: {e}")

# === URUCHOMIENIE ===
if __name__ == "__main__":
    main()
