# Department Bot

This is a Telegram bot for the School of Information Science. The bot provides information about the department, courses, and other related queries. It also offers AI assistance for answering questions.

## Table of Contents

- [Features](#features)
- [Commands](#commands)
- [Admin](#admin)
- [Setup](#setup)
- [Usage](#usage)
- [Developer](#developer)
- [License](#license)

## Features

- **AI Assistance**: Ask questions and get answers from the AI.
- **Course Information**: Get information about courses for different years and semesters.
- **FAQ**: Frequently asked questions about the department.
- **About Developer**: Information about the developer of the bot.
- **Admin Commands**: Commands for the admin to get bot information and usage statistics.
- **User Feedback**: Provide feedback about the bot or its responses.
- **Logging User Queries**: Log user queries to analyze common questions and improve the bot's responses.
- **Scheduled Messages**: Send scheduled messages or reminders to users.
- **Inline Queries**: Support inline queries to allow users to interact with the bot without starting a chat.

## Commands

- `/start`: Kickstart the conversation and explore features.
- `/ask`: Ask a question to the AI.
- `/help`: Get assistance with commands and usage.
- `/faq`: Frequently asked questions.
- `/feedback`: Provide feedback about the bot.
- `/get_bot_info`: Get information about the bot (admin only).
- `/get_bot_usage`: Get usage statistics of the bot (admin only).

## Admin

Only the admin can use the `/get_bot_info` and `/get_bot_usage` commands.

## Setup

1. Clone the repository.
    ```sh
    git clone https://github.com/kipash-prog/My-Bot.git
    cd is-bot
    ```
2. Create a `.env` file in the root directory and add the following environment variables:
    ```
    TELEGRAM_API_KEY=your_telegram_api_key
    GEMINI_API_KEY=your_gemini_api_key
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the bot:
    ```sh
    python bot.py
    ```

## Usage

- Start the bot by sending the `/start` command.
- Use the provided buttons to navigate through the options.
- Admin can use the `/get_bot_info` and `/get_bot_usage` commands to get information about the bot and its usage.

## Developer

This bot was developed by Kidus Shimelis ([https://t.me/Kipa_s](https://t.me/Kipa_s)).

Phone number: +251912063708

## License

This project is licensed under the MIT License.