import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class Athelete(Base):
    """
    Структура таблицы athelete
    """
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    # возраст атлета
    age = sa.Column(sa.Integer)
    # день рождения атлета
    birthdate = sa.Column(sa.Text)
    # пол атлета
    gender = sa.Column(sa.Text)
    # рост атлета
    height = sa.Column(sa.Float)
    # имя и фамилия атлета
    weight = sa.Column(sa.Integer)
    # вес атлета
    name = sa.Column(sa.Text)
    # количество выигранных золотых медалей у атлета
    gold_medals = sa.Column(sa.Integer)
    # количество выигранных серебрянных медалей у атлета
    silver_medals = sa.Column(sa.Integer)
    # количество выигранных бронзовых медалей у атлета
    bronze_medals = sa.Column(sa.Integer)
    # общее количество медалей у атлета
    total_medals = sa.Column(sa.Integer)
    # вид спорта, в котором выступает атлет
    sport = sa.Column(sa.Text)
    # страна которую представляем атлет
    country = sa.Column(sa.Text)


class User(Base):
    """
    Описывает структуру таблицы user, для хранения информации об зарегестрирвоанных пользователях
    """
    # задаём название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.String(36), primary_key=True)
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
    print("Добрый день! Начинаем поиск атлетов похожих на пользователя.  ")
    user_id = input("Пожалуйста, введите id пользователя: ")
    return int(user_id)


def convert_date(date_str):
    """
    Конверниуем строку с датой в формате ГГГГ-ММ-ЧЧ в объект datetime.date
    """
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date


def search_by_bd(user, session):
    """
    Ищем ближайшего к данному пользователю атлета по дате его рождения
    """
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = convert_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd

    user_bd = convert_date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
        athlete_id = id_
        athlete_bd = bd

    return athlete_id, athlete_bd


def search_by_height(user, session):
    """
    Ищет ближайшего по росту атлета к пользователю user
    """
    athletes_list = session.query(Athelete).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        if height is None:
            continue

        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height

    return athlete_id, athlete_height


def main():
    """
    Основной метод работы программы. Обрабатываем пользовательский ввод
    """
    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Такого пользователя не существует:( ")
    else:
        bd_athlete, bd = search_by_bd(user, session)
        height_athlete, height = search_by_height(user, session)
        print(
            "Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(bd_athlete, bd)
        )
        print(
            "Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height)
        )


if __name__ == "__main__":
    main()
