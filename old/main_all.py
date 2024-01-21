import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

WELCOME_TEXT = os.environ.get('GREETING')
ALLOWED_USERS = ['nemchena', 'slimshady_rost']
ALLOWED_USER_IDS = {'slimshady_rost':1861763218, 'nemchena':914118651} 


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name_to_use = user.first_name or user.username
    personal_greeting = f"{name_to_use}, {WELCOME_TEXT}"

    username = update.message.from_user.username
    if username in ALLOWED_USERS:
        ALLOWED_USER_IDS[username] = update.message.chat.id
    # ... Решта start-функції
    button = InlineKeyboardButton(text=os.environ.get('BUTTON'), callback_data="accept_rules")
    keyboard = InlineKeyboardMarkup([[button]])
    await update.message.reply_text(personal_greeting, reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "accept_rules":
        group_link = os.environ.get('GROUP_LINK')
        await context.bot.send_message(chat_id=query.from_user.id, text=f"{group_link}")

async def staff_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name_to_use = user.first_name or user.username
    if update.message.from_user.username in ALLOWED_USERS:
        await update.message.reply_text(f"current text: {name_to_use}, {WELCOME_TEXT}")
        context.user_data['change_text'] = True
    else:
        await update.message.reply_text("Sorry, it's only for me.")

async def change_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'change_text' in context.user_data and context.user_data['change_text'] and update.message.text:
        global WELCOME_TEXT
        WELCOME_TEXT = update.message.text
        await update.message.reply_text("Updated successfully!")
        context.user_data['change_text'] = False


async def notify_restart(application):
    for username, user_id in ALLOWED_USER_IDS.items():
        try:
            await application.bot.send_message(chat_id=user_id, text="Бот був перезапущений. Будь ласка, оновіть привітальний текст.")
        except Exception as e:
            print(f"Не вдалося надіслати повідомлення користувачу {username} (ID: {user_id}): {e}")



def main():
    TOKEN = os.environ.get('TOKEN')
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("staff", staff_command))
    application.add_handler(MessageHandler(None, change_text))

    loop = asyncio.get_event_loop()
    loop.create_task(notify_restart(application))
    application.run_polling()
    

if __name__ == '__main__':
    main()
