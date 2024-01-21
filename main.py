from telegram.ext import Application
from core import handlers  # Імпортування обробників
from core import config  # Імпорт конфігурацій

def main():
    application = Application.builder().token(config.TOKEN).build()

    # Додавання обробників
    handlers.register_handlers(application)

    application.run_polling()

if __name__ == '__main__':
    main()
