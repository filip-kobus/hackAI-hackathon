import json
from typing import Any, Dict
from pydantic import BaseModel
import subprocess

class ChatAdapter(BaseModel):
    send_message_endpoint: str = "http://127.0.0.1:8000/send_message"

    def send_message(self, message: str) -> Dict[str, Any]:
        payload = json.dumps({"message": message})

        result = subprocess.run(
            [
                "curl",
                "-X", "POST",
                self.send_message_endpoint,
                "-H", "Content-Type: application/json",
                "-d", payload
            ],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        transformed_responce = self._transform_response(result.stdout)
        return transformed_responce

    
    def _transform_response(self ,raw_responce :str) -> Dict[str, Any]:
        try:
            data = json.loads(raw_responce)
            split = data.get("response").split("===========")
            responce_part = split[0]
            tags_part = split[1]
            tags_part_lines = tags_part.split("\n")
            trace_index = None
            for i, tags_part_line in enumerate(tags_part_lines):
                if tags_part_line.startswith("Trace ID:"):
                    trace_index = i
                    break
            if trace_index is not None:
                tags_part_lines = tags_part_lines[:trace_index+1]
                additional = tags_part_lines[trace_index+1:]
            else:
                additional = []
        except json.JSONDecodeError:
            print("Błąd parsowania JSON")

        result_responce = {}

        if not tags_part_lines:
            result_responce["additional"] = "".join(additional)
            return result_responce  # pusta lista

        result_responce["response"] = responce_part
        for tags_part_line in tags_part_lines[1:]:
            if ": " in tags_part_line:
                key, value = tags_part_line.split(": ", 1)
                key = key.strip().replace(" ", "-")
                value = value.strip()
                result_responce[key.lower()] = value
        if "intents" not in result_responce:
            result_responce["intents"] = None
        result_responce["additional"] = "".join(additional)
        return result_responce



if __name__ == "__main__":
    adapter = ChatAdapter()
    print("Wysyłam testową wiadomość...")
    print(adapter.send_message("Witaj przyjacielu"))