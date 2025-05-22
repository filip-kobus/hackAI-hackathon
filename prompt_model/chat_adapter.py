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
            lines = data.get("response").split('\n')
            trace_index = None
            for i, line in enumerate(lines):
                if line.startswith("Trace ID:"):
                    trace_index = i
                    break
            if trace_index is not None:
                lines = lines[:trace_index+1]
                additional = lines[trace_index+1:]
            else:
                additional = []
            lines = [line for line in lines if line != "==========="]
        except json.JSONDecodeError:
            print("Błąd parsowania JSON")

        result_responce = {}

        if not lines:
            result_responce["additional"] = "".join(additional)
            return result_responce  # pusta lista

        result_responce["response"] = lines[0]
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
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