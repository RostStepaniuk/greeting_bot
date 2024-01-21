import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes
from .import config
from .import utils
import os
from dotenv import load_dotenv

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name_to_use = user.first_name or user.username
    personal_greeting = f"{name_to_use}, {config.WELCOME_TEXT}"

    username = update.message.from_user.username
    if username in config.ALLOWED_USERS:
        config.ALLOWED_USER_IDS[username] = update.message.chat.id

    button = InlineKeyboardButton(text=os.environ.get('BUTTON'), callback_data="accept_rules")
    keyboard = InlineKeyboardMarkup([[button]])
    await update.message.reply_text(personal_greeting, reply_markup=keyboard)


async def staff_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name_to_use = user.first_name or user.username
    if update.message.from_user.username in config.ALLOWED_USERS:
        cancel_button = InlineKeyboardButton(text="Cancel", callback_data="cancel_change")
        keyboard = InlineKeyboardMarkup([[cancel_button]])
        await update.message.reply_text(
            f"Current Text: \n{name_to_use}, {config.WELCOME_TEXT}",
            reply_markup=keyboard
        )
        context.user_data['change_text'] = True
    else:
        await update.message.reply_text("Sorry, it's only for me.")


# Схожим чином додаєте інші обробники

def register_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(utils.button_handler))
    application.add_handler(CommandHandler("staff", staff_command))
    application.add_handler(MessageHandler(None, utils.change_text))
    loop = asyncio.get_event_loop()
    loop.create_task(utils.notify_restart(application))