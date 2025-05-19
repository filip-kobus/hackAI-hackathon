# HackAI Project

## Overview
This project automates interactions with a web application using Selenium. It includes features such as logging in, handling shadow DOM components, and sending messages via a chat interface.

## Features
- Automated login with credentials from environment variables.
- Handling shadow DOM components for interacting with complex web elements.
- Sending messages via a chat interface.

## Requirements
- Python 3.8 or higher
- Google Chrome installed

## Installation
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables
Create a `.env` file in the project directory with the following variables:
```
USER_ID=your_user_id
PASSWORD=your_password
SMS_CODE=your_sms_code
```

## Usage
1. Run the script:
   ```bash
   python connect.py
   ```
2. Follow the prompts to interact with the application.
3. To send messages, type your message in the terminal and press Enter. Type `exit` to quit.

## Files
- `connect.py`: Main script for automation.
- `requirements.txt`: List of dependencies.
- `lokalizatory.txt`: Placeholder for additional locators (if needed).

## Notes
- Ensure that Google Chrome is installed and compatible with the `chromedriver` version.
- This script uses `chromedriver-autoinstaller` to manage the ChromeDriver version automatically.

## License
This project is licensed under the MIT License.
