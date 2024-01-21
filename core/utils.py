# Додаткові утиліти та допоміжні функції.
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from dotenv import load_dotenv
from .import config
from datetime import datetime
from .database import get_users_from_db

load_dotenv()

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    name_to_use = user.first_name or user.username
    # Якщо користувач обрав редагування вітального повідомлення
    if query.data == "edit_greeting":
        cancel_button = InlineKeyboardButton(text="Cancel", callback_data="cancel_change")
        keyboard = InlineKeyboardMarkup([[cancel_button]])
        await query.edit_message_text(
            text=f"Current Text: \n{name_to_use}, {config.WELCOME_TEXT}",
            reply_markup=keyboard
        )
        context.user_data['change_text'] = True

    # Логіка для кнопки "Users List"
    elif query.data == "show_users":
        users = get_users_from_db()
        users_list = '\n'.join([f"{user.username} - joined on {user.join_date.isoformat(timespec='seconds')}" for user in users])
        await query.edit_message_text(text=f"Users List:\n{users_list}")

    if query.data == "cancel_change":
        await query.edit_message_text("Changed cancel.")
        context.user_data['change_text'] = False

    if query.data == "accept_rules":
        group_link = config.GROUP_LINK
        await context.bot.send_message(chat_id=query.from_user.id, text=f"{group_link}")


async def change_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'change_text' in context.user_data and context.user_data['change_text'] and update.message.text:
        global WELCOME_TEXT
        WELCOME_TEXT = update.message.text
        await update.message.reply_text("Updated successfully!")
        context.user_data['change_text'] = False

# Інші допоміжні функції
        
async def notify_restart(application):
    for username, user_id in config.ALLOWED_USER_IDS.items():
        try:
            await application.bot.send_message(chat_id=user_id, text="Бот був перезапущений. Будь ласка, оновіть привітальний текст.")
        except Exception as e:
            print(f"Не вдалося надіслати повідомлення користувачу {username} (ID: {user_id}): {e}")


