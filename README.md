# HackAI API

## Overview
This project provides an API for automating interactions with a web application using Selenium. The API allows you to send messages and retrieve chat history via HTTP endpoints.

## Features
- Send messages to the chat interface.
- Retrieve the chat history.

## Requirements
- Python 3.8 or higher
- FastAPI and Uvicorn installed

## Installation
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API
Start the API server using Uvicorn:
```bash
uvicorn api.server:app --host 127.0.0.1 --port 8000 --reload
```

## Endpoints

### 1. Send Message
**POST** `/send_message`

Send a message to the chat interface.

#### Request Body:
```json
{
  "message": "Your message here"
}
```

#### Response:
```json
{
  "response": "Bot's response to your message"
}
```

### 2. Get Chat History
**GET** `/get_history`

Retrieve the chat history.

#### Response:
```json
{
  "messages": [
    "Message 1",
    "Message 2",
    "Message 3"
  ]
}
```

## Testing the API
You can test the API using tools like:
- **cURL**:
  ```bash
  curl -X POST "http://127.0.0.1:8000/send_message" -H "Content-Type: application/json" -d '{"message": "Hello"}'
  ```
  ```bash
  curl -X GET "http://127.0.0.1:8000/get_history"
  ```
- **Postman** or **Insomnia**: Use these tools to send HTTP requests and view responses.
- **Browser**: Open `http://127.0.0.1:8000/docs` to interact with the API via Swagger UI.

## Notes
- Ensure that Google Chrome is installed and compatible with the `chromedriver` version.
- This script uses `chromedriver-autoinstaller` to manage the ChromeDriver version automatically.

## License
This project is licensed under the MIT License.
