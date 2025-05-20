import datetime

# === ZAPIS ODPOWIEDZI DO PLIKU ===
def save_response_to_file(agent_message="!No message received!", mbank_message="!No message received!", importance_level=0):
    SAVEPATH="prompt_model/logs/chatlog.txt"
    with open(f"{SAVEPATH}_{importance_level}", "a", encoding="utf-8") as f:
        f.write(f"\n--- {datetime.datetime.now()}:{importance_level} ---\n")
        f.write(f"AI:\n> {agent_message}\n")
        f.write(f"mBank:\n> {mbank_message}")

# save_tool = {
#     "type": "function",
#     "function": {
#         "name": "save_response_to_file",
#         "description": "Saves responses according to their importance level, from 1 to 10.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "response": {
#                     "type": "string",
#                     "description": "Miasto, np. Warszawa"
#                 }
#             },
#             "required": ["location"]
#         }
#     }
# }

# =====================================