import psycopg2
# ... (інші імпорти)
from .models import User, Session, init_db
from sqlalchemy.exc import IntegrityError


def add_user_to_db(user_id, username, first_name, last_name, chat_id):
    session = Session()
    try:
        # Проверка, существует ли уже пользователь с данным user_id
        existing_user = session.query(User).filter(User.user_id == user_id).one_or_none()
        if existing_user is None:
            # Если пользователя нет, добавляем его
            user = User(user_id=user_id, username=username, first_name=first_name, last_name=last_name, chat_id=chat_id)
            session.add(user)
            session.commit()
        else:
            # Если пользователь уже существует, можно обновить его данные или просто пропустить
            pass
    except IntegrityError as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

def get_users_from_db():
    session = Session()
    users = session.query(User.username).all()
    
    session.close()

    users = session.query(User).all()
    for user in users:
        print(user.__dict__)  # или используйте логгер для вывода атрибутов
    return users
    