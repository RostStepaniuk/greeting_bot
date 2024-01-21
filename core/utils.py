# Додаткові утиліти та допоміжні функції.
from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv
from .import config

load_dotenv()

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

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


