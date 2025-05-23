import os
import requests
import json
import re

from faq_parser import parse_file_generator
from chat_adapter import ChatAdapter
from ai_agent import ModelChat
from tools.tools import save_response_to_file
from historyStorage import ChatHistoryStorage

# === KONFIGURACJA ===
MODEL_NAME = "gemma3:12b-it-qat"
OLLAMA_API_URL = "http://172.27.27.79:11434/api/chat"
SAVE_FILE_PATH = ""
MAX_SPLIT_RETRIES = 5
DEFAULT_MESSAGE = "Przepraszam, nie zrozumiałem. Czy mógłbyś powtórzyć?"

MAX_MESSAGES_PER_QUESTION = 5

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
    agent = ModelChat(MODEL_NAME, OLLAMA_API_URL)
    chat_adapter = ChatAdapter()
    faq_file = os.path.abspath(r'data/mbank-pytania.md')
    # === INTERFEJSY ===
    # TO-DO żeby tutaj podpinać rzeczy, a ich implementacja była wymienialna
    def _generate_message(system_prompt: str, input_message: str) -> str:
        try:
            if agent.system_prompt is None:    
                agent.set_system_prompt(system_prompt)
            agent_response = agent.send_prompt(input_message)
            agent_response_formatted = format_response(agent_response)
        except Exception as e:
            print(f"Error while generating agent message: {e}")
            agent_response_formatted = "Nie zrozumiałem. Czy mógłbyś powtórzyć?"
        return agent_response_formatted
    
    def _send_start_signal(system_prompt: str) -> str:
        return _generate_message(system_prompt, "[START]")

    def _send_message_to_chatbot(message: str) -> str:
        return chat_adapter.send_message(message)
    
    def _split_message_parts(agent_response_formatted: str) -> tuple[str, str]:
        agent_response_formatted = re.sub(r'\n+', '\n', agent_response_formatted)
        lines = agent_response_formatted.strip().split('\n')
        key_words = ['PROCES_MYSLOWY:', 'ODPOWIEDZ:']
        
        if len(lines) < len(key_words):
            raise ValueError("Za mało kompentów odpowiedzi agenta!")      
        for i in range(len(key_words)):
            words = lines[i].split(' ')
            if words[0] != key_words[i]:
                raise ValueError("Niepoprawny komponent w odpowiedzi agenta!")  
            lines[i] = words[1:]         
        return ' '.join(lines[0]), ' '.join(lines[1]).strip()

     #============ Model workloop ================
    print(f"=== Starting {MODEL_NAME}... ===")
    counter = 0
    for chosen_faq_question in parse_file_generator(faq_file):
        counter += 1
        chat_history_storage = ChatHistoryStorage(chosen_faq_question)
        storage_index = chat_history_storage.get_number_of_files()
        # GET_NUMBER_OF_FILES nie uwzględnia plików innych niż json!!!!
        if storage_index >= counter:
            continue
        system_prompt = _get_system_prompt(chosen_faq_question)

        # === Obsługa pierwszego komunikatu ===
        first_message_processed = False
        for attempt in range(MAX_SPLIT_RETRIES):
            try:
                raw_agent_response = _send_start_signal(system_prompt)
                thought_process, first_message = _split_message_parts(raw_agent_response)
                first_message_processed = True
                break
            except ValueError as e:
                print(f"Błąd podczas przetwarzania odpowiedzi agenta (próba {attempt + 1}/{MAX_SPLIT_RETRIES}): {e}")
                if attempt == MAX_SPLIT_RETRIES - 1:
                    print("Nie udało się przetworzyć odpowiedzi agenta po maksymalnej liczbie prób.")
                    break

        if not first_message_processed:
            first_message = DEFAULT_MESSAGE

        print("\nAI:\n" + first_message)
        received_message = _send_message_to_chatbot(first_message)
        print("\nmBank:\n" + str(received_message))
        chat_history_storage.save_dialog_fragment(model_message=first_message, chatbot_answer=received_message)

        # === Obsługa kolejnych komunikatów ===
        for i in range(MAX_MESSAGES_PER_QUESTION):
            message_processed_in_loop = False
            for attempt in range(MAX_SPLIT_RETRIES):
                try:
                    raw_agent_response_loop = _generate_message(system_prompt, received_message['response'])
                    thought_process, generated_message = _split_message_parts(raw_agent_response_loop)
                    message_processed_in_loop = True
                    break
                except ValueError as e:
                    print(f"Błąd podczas przetwarzania odpowiedzi agenta w pętli (próba {attempt + 1}/{MAX_SPLIT_RETRIES}): {e}")
                    if attempt == MAX_SPLIT_RETRIES - 1:
                        print("Nie udało się przetworzyć odpowiedzi agenta w pętli po maksymalnej liczbie prób.")
                        break

            if not message_processed_in_loop:
                generated_message = DEFAULT_MESSAGE

            print("\nAI:\n" + generated_message)
            received_message = _send_message_to_chatbot(generated_message)
            print("\nmBank:\n" + str(received_message))
            chat_history_storage.save_dialog_fragment(model_message=generated_message, chatbot_answer=received_message)
            if(received_message['response'] == "RESET SUCCESSFULL"):
                break
        chat_history_storage.save_to_file()
        _send_message_to_chatbot("[RESET]")

    # # Do zaimplementowania wstrzykiwanie odpowiedniego FAQ i historii chatu!!!
    # faq = "Minimalna kwota kredytu to 10zł"
    # historia_chatu = ""
    # system_prompt = _get_system_prompt(faq, historia_chatu)

    # try:
    #     agent_response = agent.send_prompt(system_prompt, "[START]")
    #     agent_response_formatted = format_response(agent_response)
    #     print("\nAI:\n" + agent_response_formatted)

    #     mbank_answer = chat_adapter.send_message(agent_response_formatted)
    #     print("\nmBank:\n" + str(mbank_answer))

    #     save_response_to_file(agent_response_formatted, mbank_answer)

    # except Exception as e:
    #     print(f"Error: {e}")



def _get_system_prompt(faq_context: str) -> str:
    system_prompt = f"""
    KONTEKST_FAQ:
    {faq_context}

    CEL:
    Jesteś systemem do zadawania pytań konsultantowi bankowemu na podstawie informacji zawartych w KONTEKST_FAQ. Twoim zadaniem jest prowadzenie rozmowy poprzez zadawanie konkretnych pytań dotyczących usług bankowych.

    ZASADY:
    1. Na wiadomości "[START]" lub "RESET SUCCESSFULL" MUSISZ zadać pytanie ŚCIŚLE dotyczące informacji zawartej w KONTEKST_FAQ.
    2. W przypadku otrzymania wiadomości "Jesteś zablokowany!!!" MUSISZ odpowiedzieć jedynie "[RESET]".
    3. Jeżeli otrzymasz odpowiedź wskazującą na niezrozumienie lub odmowę ("Chcę mieć pewność, że dobrze zrozumiałem", "Nie mogę udzielić odpowiedzi", "Przepraszam, ale nie mogę"), przekształć swoje pytanie i zadaj je w innej formie.
    4. NIE dziękuj konsultantowi - skup się tylko na zadawaniu pytań.
    5. Zadawaj konkretne, jasne pytania dotyczące usług bankowych z KONTEKST_FAQ.
    6. KAŻDA Twoja wiadomość powinna zawierać sekcje opisane w FORMAT_ODPOWIEDZI.

    PLAN_DZIAŁANIA:
    1. Przeanalizuj otrzymaną wiadomość.
    2. Na podstawie KONTEKST_FAQ zadaj następne pytanie dotyczące usług bankowych.
    3. Jeśli potrzeba, przekształć pytanie w bardziej zrozumiałą formę.

    FORMAT_ODPOWIEDZI:
    - KONIECZNIE. Krótki proces myślowy dotyczący wyboru kolejnego pytania. KONIECZNIE MUSI być to poprzedzone zwrotem "PROCES_MYSLOWY: ".
    - KONIECZNIE. Pytanie do konsultanta bankowego. KONIECZNIE MUSI być to poprzedzone zwrotem "ODPOWIEDZ: ".
    """

    return system_prompt



# === URUCHOMIENIE ===
if __name__ == "__main__":
    main()