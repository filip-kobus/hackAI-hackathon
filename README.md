# HackAI: Testing mBank AI Resilience ~ norbgsoft

## Project Description

**HackAI** is a project designed to conduct a controlled attempt to "hack" mBank's artificial intelligence. In our project we developed software for automated communication with the AI model and for evaluating its responses. Our approach was to record as many articial chat dialogs as we could in order to maximalize chance of finding interesting chatbot stumbles. The project consists of several key modules:

* **`api`**: Utilizes **Selenium** for automated access to mBank's chat, bypassing browser interaction. This module must be launched before running `faq_executor`, which uses the API to communicate with the chatbot.
* **`faq_executor`**: This module, based on questions from mBank's FAQ section, conducts a natural dialogue with the AI using our **Gemma3** model. Thanks to this LLM, we successfully automated the analysis of all FAQ questions and their variants.
Running this module results in turning on our ai agent which starts chatting with mBank chatbot performing conversation related to chosen topic from `data/mbank-pytania.md`. Dialogs are saved in json files in `output` folder.
* **`scenario_executor`**: Similar to `faq_executor`, this module uses an LLM to attempt to trick the mBank chat based on predefined scenarios.
Running this module results in turning on our ai agent which starts chatting with mBank chatbot performing conversation accordingly to scenarios in `data/scenariusze.md` file. Dialogs are saved in json files in `scenarios_output` folder.
* **`grade_executor`**: A module for preliminary analysis of conversations with mBank's AI, also using our **Gemma3** model. It sorts conversations based on the lowest AI response scores, allowing us to quickly identify instances where the chatbot didn't provide ideal answers.
Running this module results in turning on our ai agent whose task is to grade conversations from json files in `output` folder. Graded dialogs are saved in `graded` folder.

## Requirements

* **Python 3.8** or higher
* All required packages are listed in the `requirements.txt` file.
* Ollama with downloaded gemma3:12b model (can be aquired with `ollama pull gemma3:12b-it-qat`)
## Installation

1.  Clone this repository.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Modules

### Running the API

To enable the API for connecting to the mBank website, run:

```bash
python -m src.run_selenium
```

#### Sending a Request (API)

**POST** `/send_message`

Sends a query to the interface.

**Request Body:**

```json
{
  "message": "Your message here"
}
```

**Response:**

```json
{
  "response": "Bot's response to your message"
}
```

### Running `faq_executor`
**Before running any executor modules please turn on ollama server with  `ollama serve` command.**
**Before running this module, make sure the API is enabled!**

```bash
python -m src.executors.faq_executor
```

### Running `scenario_executor`

**Similar to `faq_executor`, enabling the API is essential before running this module!**

```bash
python -m src.executors.scenario_executor
```

### Running `grade_executor`

```bash
python -m src.executors.grading_executor
```

## Important Notes

* Ensure that **Google Chrome** is installed and compatible with the **`chromedriver`** version.
* The script uses **`chromedriver-autoinstaller`** to automatically manage the `chromedriver` version.

## License

This project is licensed under the **MIT License**.