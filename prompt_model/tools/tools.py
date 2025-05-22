import datetime

# === ZAPIS ODPOWIEDZI DO PLIKU ===
class ChatHistoryStorage:
    def __init__(self):
        self.chat_history = []

    def save_dialog_fragment(self, agent_message, mbank_message):
        self.chat_history.append({
            "agent_message": agent_message,
            "mbank_message": mbank_message
        })

    def save_to_file(self):
        save_path = f"prompt_model/logs/chatlog_{datetime.datetime.nowe().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(f'{save_path}', "a", encoding="utf-8") as f:
            for fragment in self.chat_history:
                f.write(f"Agent: {fragment['agent_message']}\n")
                f.write(f"mBank: {fragment['mbank_message']}\n")
                f.write("\n")
