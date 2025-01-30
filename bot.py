import os
import logging
import requests
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, CallbackQueryHandler
from dotenv import load_dotenv
import google.generativeai as genai

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta2/models/gemini-1.5-flash:generateText"
)

if not TELEGRAM_API_KEY or not GEMINI_API_KEY:
    raise ValueError("TELEGRAM_API_KEY and GEMINI_API_KEY must be set in the .env file.")

# Configure AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Sample FAQs
FAQS = {
    "⚪️Where is the department located?\n": (
        "✅The School of Information Science is located at 6K FBE Campus.\n\n"
        "📍 [View on Google Maps](https://maps.app.goo.gl/3nX9U6cePwRnRHL5A)"
    ),
    "⚪️What are the criteria for joining the department?\n": (
        "✅Students are admitted based on a department-specific cutoff, which is determined annually. \n"
        "The cutoff is calculated using:\n\n"
        "🎯50% Entrance Exam Score\n"
        "🎯50% GPA\n"
        "Please note that the cutoff may vary from year to year based on departmental decisions.‼️‼️ \n"
    ),
    "⚪️How long is the course duration?": "✅The program takes four years, including the freshman year.",
}

# Dictionary to store user actions and track first-time users
user_actions = {}
first_time_users = set()


async def track_user_action(user_id: int, action: str) -> None:
    """Track user actions for analytics."""
    if user_id not in user_actions:
        user_actions[user_id] = []
    user_actions[user_id].append(action)


async def start(update: Update, context: CallbackContext) -> None:
    """Handle the /start command."""
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    if user_id not in first_time_users:
        first_time_users.add(user_id)
        await update.message.reply_text(
            f"Hi, {username} ! Welcome to the School of Information Science Department Bot. I'm your friendly assistant. How can I help you today?"
        )

    keyboard = [
        [
            InlineKeyboardButton("AI Assistance", callback_data="ai_assistance"),
            InlineKeyboardButton("Course", callback_data="course"),
        ],
        [
            InlineKeyboardButton("About Developer", callback_data="about_developer"),
            InlineKeyboardButton("FAQ", callback_data="faq"),
        ],
        [InlineKeyboardButton("Feedback", callback_data="feedback")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)


async def show_exit_option(update: Update, context: CallbackContext) -> None:
    """Show exit option to the user."""
    keyboard = [[InlineKeyboardButton("Exit", callback_data="end")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Do you need anything else?", reply_markup=reply_markup)


async def faq(update: Update, context: CallbackContext) -> None:
    """Handle the FAQ command."""
    keyboard = [
        [InlineKeyboardButton(question, callback_data=f"faq_{i}")]
        for i, question in enumerate(FAQS.keys())
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text="Choose a question:", reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()
    data = query.data

    try:
        if data == "ai_assistance":
            await query.message.reply_text(text="Please type your question:")
            context.user_data["awaiting_question"] = True
        elif data == "course":
            keyboard = [
                [
                    InlineKeyboardButton("2nd Year", callback_data="2nd_year"),
                    InlineKeyboardButton("3rd Year", callback_data="3rd_year"),
                    InlineKeyboardButton("4th Year", callback_data="4th_year"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(text="Choose your year:", reply_markup=reply_markup)
        elif data == "about_developer":
            await query.message.reply_text(text="This bot was developed by kidus shimelis(@kipa_s).")
            await show_exit_option(query, context)
        elif data == "faq":
            await faq(query, context)
        elif data.startswith("faq_"):
            index = int(data.split("_")[1])
            question = list(FAQS.keys())[index]
            answer = FAQS[question]
            await query.message.reply_text(text=f"{question}\n{answer}")
            await show_exit_option(query, context)
        elif data in ["2nd_year", "3rd_year", "4th_year"]:
            keyboard = [
                [
                    InlineKeyboardButton("1st Semester", callback_data=f"{data}_1st_semester"),
                    InlineKeyboardButton("2nd Semester", callback_data=f"{data}_2nd_semester"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                text=f" Selected year : {data.replace('_', ' ').title()}. Choose your semester:",
                reply_markup=reply_markup,
            )
        elif data == "2nd_year_1st_semester":
            keyboard = [
                [InlineKeyboardButton("Management", url="https://t.me/man_course")],
                [InlineKeyboardButton("Accounting", url="https://t.me/acc_course")],
                [InlineKeyboardButton("Discrete Mathematics", url="https://t.me/discrete_math_course")],
                [InlineKeyboardButton("Foundation of Information System", url="https://t.me/fis_course")],
                [InlineKeyboardButton("Introduction to Database", url="https://t.me/db_course1")],
                [InlineKeyboardButton("Advanced Computer Programming", url="https://t.me/acp_course")],
                [InlineKeyboardButton("Exit", callback_data="end")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(text="Choose a course:", reply_markup=reply_markup)
        elif data == "2nd_year_2nd_semester":
            keyboard = [
                [InlineKeyboardButton("Introductory Statistics", url="https://t.me/+JhEeDHh4kNswMjc8")],
                [InlineKeyboardButton("Economics", url="https://t.me/+kXEicAbCcywxOGI0")],
                [
                    InlineKeyboardButton(
                        "Introduction to Information Storage and Retrieval",
                        url="https://t.me/+ljxV8ycwetZmMDlk",
                    )
                ],
                [InlineKeyboardButton("Data Structure and Algorithm", url="https://t.me/+H2xvF45sekVmZWZk")],
                [InlineKeyboardButton("Object Oriented Programming", url="https://t.me/+Y2i1mmnOS_M1M2U0")],
                [InlineKeyboardButton("Advanced Database Systems", url="https://t.me/+l31cuBsg9K5jNWU0")],
                [InlineKeyboardButton("Exit", callback_data="end")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(text="Choose a course:", reply_markup=reply_markup)
        elif data == "3rd_year_1st_semester":
            keyboard = [
                [
                    InlineKeyboardButton(
                        "Introduction to System Analysis and Design", url="https://t.me/+ssWJIwAKf1liNTQ0"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Computer Architecture and operating system", url="https://t.me/+FZuPpr68X-M4MjQ0"
                    )
                ],
                [InlineKeyboardButton("Networking", url="https://t.me/+-v31sfMr155hNWY0")],
                [InlineKeyboardButton("Research Method", url="https://t.me/+0sKOOKneWvYwZmE0")],
                [InlineKeyboardButton("Event Driven Programming", url="https://t.me/+zdeVGa761vY1ZDI0")],
                [InlineKeyboardButton("Internet Programming", url="https://t.me/+Ti48IA7umC1jNzU0")],
                [InlineKeyboardButton("Exit", callback_data="end")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(text="Choose a course:", reply_markup=reply_markup)
        elif data == "3rd_year_2nd_semester":
            keyboard = [
                [InlineKeyboardButton("Administration of Systems and Networks", url="https://t.me/admin_sys_net")],
                [InlineKeyboardButton("E-commerce", url="https://t.me/ecommerce_course")],
                [InlineKeyboardButton("Information System Security", url="https://t.me/iss_course")],
                [InlineKeyboardButton("Advanced Internet Programming", url="https://t.me/adv_internet_prog")],
                [InlineKeyboardButton("Mobile Computing", url="https://t.me/mobile_computing")],
                [InlineKeyboardButton("Object Oriented System Analysis and Design", url="https://t.me/oosad")],
                [InlineKeyboardButton("Exit", callback_data="end")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(text="Choose a course:", reply_markup=reply_markup)
        elif data == "4th_year_1st_semester":
            keyboard = [
                [InlineKeyboardButton("Inclusiveness", url="https://t.me/project_management")],
                [InlineKeyboardButton("Intoduction to Artificial Intelligence", url="https://t.me/artificial_intelligence")],
                [
                    InlineKeyboardButton(
                        "Information System Project Management", url="https://t.me/project_management"
                    )
                ],
                [InlineKeyboardButton("Human-Computer Interaction", url="https://t.me/hci")],
                [InlineKeyboardButton("Exit", callback_data="end")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(text="Choose a course:", reply_markup=reply_markup)
        elif data == "4th_year_2nd_semester":
            keyboard = [
                [InlineKeyboardButton("Global Trends", url="https://t.me/isp")],
                [InlineKeyboardButton("Knowledge Management", url="https://t.me/knowledge_management")],
                [
                    InlineKeyboardButton(
                        "Management Of Information System and Services", url="https://t.me/iss"
                    )
                ],
                [InlineKeyboardButton("Enterprise Systems", url="https://t.me/it_audit")],
                [
                    InlineKeyboardButton(
                        "Introduction to Data Science and Analytics", url="https://t.me/internship"
                    )
                ],
                [InlineKeyboardButton("History", url="https://t.me/ethical_hacking")],
                [InlineKeyboardButton("Exit", callback_data="end")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(text="Choose a course:", reply_markup=reply_markup)
        elif data == "start_over":
            await start(query, context)
        elif data == "end":
            await query.message.reply_text(text="Thank you! Have a great day!🤝በርታ/ቺ")
            await start(query, context)
        elif data == "feedback":
            await feedback(query, context)
        else:
            await show_exit_option(query, context)
    except Exception as e:
        logger.error(f"Error handling button click: {e}")
        await query.message.reply_text("An error occurred. Please try again.")


async def show_continue_options(update: Update, context: CallbackContext) -> None:
    """Show continue options to the user."""
    keyboard = [[InlineKeyboardButton("Exit", callback_data="end")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Do you need anything else?", reply_markup=reply_markup)

<<<<<<< HEAD

=======
>>>>>>> 269fddacba4ff2a5ead09b3bbf766ca8a2a58b79
async def help_command(update: Update, context: CallbackContext) -> None:
    """Handle the /help command."""
    help_text = (
        "/start: Kickstart the conversation and explore features.\n"
        "/ask: Ask a question to the AI.\n"
        "/help: Get assistance with commands and usage.\n"
        "/faq: Frequently asked questions.\n"
        "feedback: Send feedback to the developer.\n"
    )
    await update.message.reply_text(help_text)


async def ask(update: Update, context: CallbackContext) -> None:
    """Handle the /ask command."""
    context.user_data["awaiting_question"] = True
    await update.message.reply_text("Please type your question:")


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages."""
    user_id = update.message.from_user.id
    try:
        if context.user_data.get("awaiting_question"):
            question = update.message.text
            # Fetch answer from AI
            answer = get_ai_response(question)
            await update.message.reply_text(f"{answer}")
            await show_exit_option(update, context)
            context.user_data["awaiting_question"] = True  # Keep awaiting for the next question
            await track_user_action(user_id, "ask_question")
        elif context.user_data.get("awaiting_feedback"):
            feedback_text = update.message.text
            admin_chat_id = os.getenv("ADMIN_CHAT_ID")
            if admin_chat_id:
                await context.bot.send_message(
                    chat_id=admin_chat_id,
                    text=f"Feedback from {update.message.from_user.username}: {feedback_text}",
                )
                await update.message.reply_text("Thank you for your feedback!")
            else:
                await update.message.reply_text("Failed to send feedback. Admin chat ID is not set.")
            context.user_data["awaiting_feedback"] = False
            await track_user_action(user_id, "send_feedback")
            await start(update, context)
        elif update.message.text.startswith("/"):
            await update.message.reply_text("Unknown command. Please use /help to see the available commands.")
            await help_command(update, context)
            await track_user_action(user_id, "send_message")
        else:
            await update.message.reply_text("Please use the /ask command to ask a question.")
            await show_exit_option(update, context)
            await track_user_action(user_id, "send_message")
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text("An error occurred. Please try again.")


# Function to get AI response from the given API
def get_ai_response(question: str) -> str:
    """Get AI response from the given API."""
    response = model.generate_content(question)
    return response.text


# Admin username
ADMIN_USERNAME = "ADD_BOT_ADMIN_USER_NAME"


def is_admin(username: str) -> bool:
    """Check if the user is an admin."""
    return username == ADMIN_USERNAME


async def get_bot_info(update: Update, context: CallbackContext) -> None:
    """Handle the /get_bot_info command."""
    username = update.message.from_user.username
    if not is_admin(username):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    bot_info = await context.bot.get_me()
    info_text = (
        f"Bot ID: {bot_info.id}\n"
        f"Bot Name: {bot_info.first_name}\n"
        f"Bot Username: @{bot_info.username}\n"
        f"Bot Can Join Groups: {bot_info.can_join_groups}\n"
        f"Bot Can Read All Group Messages: {bot_info.can_read_all_group_messages}\n"
        f"Bot Supports Inline Queries: {bot_info.supports_inline_queries}"
    )
    await update.message.reply_text(info_text)


async def get_bot_usage(update: Update, context: CallbackContext) -> None:
    """Handle the /get_bot_usage command."""
    username = update.message.from_user.username
    if not is_admin(username):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    total_users = len(user_actions)
    action_counts = {}
    for actions in user_actions.values():
        for action in actions:
            if action not in action_counts:
                action_counts[action] = 0
            action_counts[action] += 1

    most_common_action = max(action_counts, key=action_counts.get) if action_counts else "None"
    usage_text = (
        f"Total Users: {total_users}\n"
        f"Most Common Action: {most_common_action}\n"
        f"Action Counts: {action_counts}"
    )
    await update.message.reply_text(usage_text)


async def feedback(update: Update, context: CallbackContext) -> None:
    """Handle the /feedback command."""
    user_id = update.message.from_user.id
    context.user_data["awaiting_feedback"] = True
    await update.message.reply_text("Please type your feedback:")
    await track_user_action(update.message.from_user.id, "send_feedback")


def main() -> None:
    """Start the bot."""
    if not TELEGRAM_API_KEY:
        raise ValueError("TELEGRAM_API_KEY is not set")

    application = Application.builder().token(TELEGRAM_API_KEY).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", ask))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("faq", faq))
    application.add_handler(CommandHandler("get_bot_info", get_bot_info))
    application.add_handler(CommandHandler("get_bot_usage", get_bot_usage))
    application.add_handler(CommandHandler("feedback", feedback))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Use the correct method to start polling
    try:
        application.run_polling()
    except telegram.error.Conflict as e:
        logger.error(f"Conflict error: {e}")
        logger.info("Make sure that only one bot instance is running.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()