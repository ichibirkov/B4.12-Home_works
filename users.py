import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user, для хранения информации об зарегестрирвоанных пользователях
    """
    # задаём название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.INTEGER, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # почта пользователя
    email = sa.Column(sa.Text)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # рост пользователя
    height = sa.Column(sa.Float)


def connect_db():
    """
    Устанавливаем соеденение к базе данных, возвращаем объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    # создаём фабрику сессию
    session = sessionmaker(engine)
    return session()


def request_data():
    """
    Запрашиваем у пользователя данные и добавляем их в список users
    """
    # приветствие
    print("Добрый день! Хочу записать Ваши данные")
    # запрашиваем данные у пользователя
    first_name = input("Введите своё имя: ")
    last_name = input("Введите сою фамилию: ")
    gender = input("Ваш пол - Male или Female?: ")
    email = input("Необходимо указать Вашу почту: ")
    birthdate = input("Введите пожалуйста дату Вашего рождения: ")
    height = input("Укажите Ваш рост: ")
    # созадём нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user


def main():
    """
    Основной метод работы программы. Обрабатываем пользовательский ввод
    """
    session = connect_db()
    user = request_data()
    # добавляем нового пользователя
    session.add(user)
    # сохраняем все изменения
    session.commit()
    print("Спасибо, данные сохранены!")


if __name__ == "__main__":
    main()
