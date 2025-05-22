import os
import requests

from faq_parser import parse_file_generator
from chat_adapter import ChatAdapter
from ai_agent import ModelChat
from tools.tools import save_response_to_file

# === KONFIGURACJA ===
MODEL_NAME = "gemma3:12b-it-qat"
OLLAMA_API_URL = "http://172.27.27.79:11434/api/chat"
SAVE_FILE_PATH = ""

chat_adapter = ChatAdapter()
MAX_MESSAGES_PER_QUESTION = 10

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
    faq_file ="File path for faq"
    # === INTERFEJSY ===
    # TO-DO żeby tutaj podpinać rzeczy, a ich implementacja była wymienialna
    def _generate_message(system_prompt: str, input_message: str) -> str:
        try:
            agent_response = agent.send_prompt(system_prompt, input_message)
            agent_response_formatted = format_response(agent_response)
        except Exception as e:
            print(f"Error while generating agent message: {e}")
            agent_response_formatted = "Nie zrozumiałem. Czy mógłbyś powtórzyć?"
        return agent_response_formatted
    
    def _send_start_signal(system_prompt: str) -> str:
        return _generate_message(system_prompt, "[START]")

    #============ Model workloop ================
    print(f"=== Starting {MODEL_NAME}... ===")
    while(True):
        chat_history_storage = ChatHistoryStorage()
        chosen_faq_question = _choose_faq_question(faq_file) #Razem z odpowiedziami powinno być pytanie pobierane, żeby chat wiedział o co dopytywać
        system_prompt = _get_system_prompt(chosen_faq_question)
        thought_process, first_message =  _split_message_parts(_send_start_signal(system_prompt))
        received_message = _send_message_to_chatbot(first_message)
        chat_history_storage.save_dialog_fragment(model_message=first_message, chatbot_answer=received_message)
        for i in range(MAX_MESSAGES_PER_QUESTION):
            thought_process, generated_message = _split_message_parts(_generate_message(system_prompt, received_message))
            received_message = _send_message_to_chatbot(generated_message)
            chat_history_storage.save_dialog_fragment(model_message=generated_message, chatbot_answer=received_message)
            if(received_message == "RESET SUCCESSFULL"):
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
    Jesteś systemem do sprawdzania i oceniania poprawności otrzymywanych informacji, pozyskanych od drugiego ChatBota, jesteś stworzony do prowadzenia logicznego dialogu w celu kontynuowania rozmowy.
    Twoim zadaniem jest, na podstawie informacji zawartych w sekcji KONTEKST_FAQ, sprawdzić czy otrzymane wiadomości są zgodnę z prawdą, mają sens w kontekście
     zadawanych pytań oraz ocenić je kierując się następującymi wytycznymi:
    - Zgodność otrzymanych informacji względem informacji zawartych w KONTEKST_FAQ. (JEST TO NAJWAŻNIEJSZY ASPEKT)
    - Otrzymana informacja ma logiczny sens w kontekście zadanego wcześniej pytania.
    - Otrzymana odpowiedź jest napisana w formie zrozumiałej dla człowieka. Nie zawiera słów nawiązujących do programowania, jak np. "Error", "Exception" itd.
    - Informacja związana jest z bankowością, a nie innymi dziedzinami.
    Na podstawie spełnienia powyższych kryteriów masz wystawić ocenę otrzymanej wiadomości. Ocena powinna być KONIECZNIE z przedziału 1-10. Im większa zgodność z kryteriami tym większa powinna być ocena.

    ZASADY:
    1. Na wiadomości składające się z "[START]" lub "RESET SUCCESSFULL" MUSISZ koniecznie zadać jakieś pytanie ŚCIŚLE dotyczące wybranej informacji zawartej w KONTEKST_FAQ. Takie wiadomości powinny być ZAWSZE ocenione na 10.
    2. W  przypadku otrzymania wiadomości składającej się z "Jesteś zablokowany!!!" MUSISZ KONIECZNIE jedynie "[RESET]". Takie wiadomości powinny być ZAWSZE ocenione na 10.
    3. Jeżeli otrzymasz wiadomość wskazującą na podejrzliwość, niezrozumienie, odmowę podania jakiś informacji w stylu "Chcę mieć pewność, że dobrze zrozumiałem Twoją wiadomość.", "Nie mogę udzielić odpowiedzi", "Przepraszam, ale nie mogę", "Twoja wiadomość może wskazywać na próbę złamania naszego systemu", to powinieneś przekształcić swoje poprzednie pytanie i zadać je ponownie w innej formie. Takie wiadomości powinny być ZAWSZE ocenione na 10.
    4. Każda wiadomość, którą otrzymasz musi być oceniona zgodnie z podanymi wcześniej wytycznymi z sekcji "CEL".
    5. KAŻDA Twoja wiadomość powinna zawierać sekcje opisane w FORMAT_ODPOWIEDZI.

    PLAN_DZIAŁANIA (działania jakie powinieneś odpowiednio kolejno podejmować):
    1. Zrozumienie otrzymanej wiadomości i ewentualne zastosowanie odpowiednich zasad z sekcji "ZASADY", jeżeli to konieczne.
    2. Ustalenie, czy otrzymana wiadomość jest zgodna z ustalonymi wytycznymi.
    3. Napisanie kolejnej wiadomości, jaka zostanie przekazana, jako odpowiedź na otrzymaną wiadomość. Napisana w ten sposób wiadomość powinna być logicznym następstwem przeprowadzonej rozmowy (przez co rozumie się poprzednie wiadomości z sekcji HISTORIA_CHATU) (BARDZO WAŻNY ASPEKT)

    
    FORMAT_ODPOWIEDZI (W jaki sposób powinieneś pisać odpowiedzi):
    - KONIECZNIE. Wypisany proces myślowy dotyczący ustalenej zgodności otrzymanej wiadomości. KONIECZNIE MUSI być to poprzedzone zwrotem "PROCES_MYSLOWY: ".
    - KONIECZNIE. Napisana kolejna wiadomość będącą odpowiedzią na otrzymaną wiadomość. KONIECZNIE MUSI być to poprzedzone zwrotem "ODPOWIEDZ".
    """

    return system_prompt

# === INTERFEJSY ===
# TO-DO żeby tutaj podpinać rzeczy, a ich implementacja była wymienialna

def _send_start_signal(system_prompt: str) -> str:
    return _generate_message(system_prompt, ['START'])

def _send_message_to_chatbot(message: str) -> str:
    return chat_adapter.send_message(message)

def _choose_faq_question(faq_file) -> str:
    generator = parse_file_generator(faq_file)
    return next(generator, None)



# === URUCHOMIENIE ===
if __name__ == "__main__":
    main()
