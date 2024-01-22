import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes
from .import config
from .import utils
import os
from dotenv import load_dotenv
from .import database

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    # Виклик функції для додавання користувача до БД
    database.add_user_to_db(
        user.id, user.username, user.first_name, user.last_name, update.message.chat.id
    )
    name_to_use = user.first_name or user.username
    # Загрузка приветственного текста из файла конфигурации
    WELCOME_TEXT = utils.retrieve_welcome_text()
    personal_greeting = f"{name_to_use}, {WELCOME_TEXT}"
    username = update.message.from_user.username
    if username in config.ALLOWED_USERS:
        config.ALLOWED_USER_IDS[username] = update.message.chat.id

    button = InlineKeyboardButton(text=os.environ.get('BUTTON'), callback_data="accept_rules")
    keyboard = InlineKeyboardMarkup([[button]])
    await update.message.reply_text(personal_greeting, reply_markup=keyboard)


async def staff_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.username in config.ALLOWED_USERS:
        greeting_button = InlineKeyboardButton(text="Greeting Message", callback_data="edit_greeting")
        users_list_button = InlineKeyboardButton(text="Users List", callback_data="show_users")
        keyboard = InlineKeyboardMarkup([[greeting_button, users_list_button]])

        # Відправка повідомлення з кнопками
        await update.message.reply_text("Choose function:", reply_markup=keyboard)
    else:
        await update.message.reply_text("option is only for admin.")


# Схожим чином додаєте інші обробники
        


def register_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(utils.button_handler))
    application.add_handler(CommandHandler("staff", staff_command))
    application.add_handler(MessageHandler(None, utils.change_text))
    loop = asyncio.get_event_loop()
    loop.create_task(utils.notify_restart(application))
    utils.load_welcome_text()