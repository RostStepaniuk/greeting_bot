from telegram.ext import Application
from core import handlers  # Імпортування обробників
from core import config  # Імпорт конфігурацій
from core import models

def main():
    application = Application.builder().token(config.TOKEN).build()

    # Додавання обробників
    handlers.register_handlers(application)

    models.init_db()
    application.run_polling()

if __name__ == '__main__':
    main()
