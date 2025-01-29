# Department Bot

This is a Telegram bot for the School of Information Science. The bot provides information about the department, courses, and other related queries. It also offers AI assistance for answering questions.

## Features

- **AI Assistance**: Ask questions and get answers from the AI.
- **Course Information**: Get information about courses for different years and semesters.
- **FAQ**: Frequently asked questions about the department.
- **About Developer**: Information about the developer of the bot.
- **Admin Commands**: Commands for the admin to get bot information and usage statistics.

## Commands

- `/start`: Kickstart the conversation and explore features.
- `/ask`: Ask a question to the AI.
- `/help`: Get assistance with commands and usage.
- `/faq`: Frequently asked questions.
- `/get_bot_info`: Get information about the bot (admin only).
- `/get_bot_usage`: Get usage statistics of the bot (admin only).

## Admin

Only the admin can use the `/get_bot_info` and `/get_bot_usage` commands.

## Setup

1. Clone the repository.
2. Create a `.env` file in the root directory and add the following environment variables:
    ```
    TELEGRAM_API_KEY=your_telegram_api_key
    GEMINI_API_KEY=your_gemini_api_key
    ```
3. Run the bot:
    ```
    python bot.py
    ```

## Usage

- Start the bot by sending the `/start` command.
- Use the provided buttons to navigate through the options.
- Admin can use the `/get_bot_info` and `/get_bot_usage` commands to get information about the bot and its usage.

## Developer

This bot was developed by Kidus Shimelis ((https://t.me/Kipa_s)).

phone number:- +251912063708

## License

This project is licensed under the MIT License.
