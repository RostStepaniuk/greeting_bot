from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = "Вітаю! Ось основні правила групи: ..."
    button = InlineKeyboardButton(text="Я все зрозумів", callback_data="accept_rules")
    keyboard = InlineKeyboardMarkup([[button]])
    await update.message.reply_text(welcome_message, reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "accept_rules":
        group_link = os.environ.get('GROUP_LINK')
        await context.bot.send_message(chat_id=query.from_user.id, text=f"Ось посилання на групу: {group_link}")

def main():
    TOKEN = os.environ.get('TOKEN')
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()




#TOKEN = "6816938238:AAG0oJhK3Y4G_bgGZmmu8vO_6Qs46suQmHo"
    