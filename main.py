from flask import Flask, render_template
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars.sqlite")
    app.run()


def add_user_func(name, surname=None, age=None, position=None, speciality=None,
                  address=None, email=None, hashed_password=None):
    user = User()
    user.surname = surname
    user.name = name
    user.age = age
    user.position = position
    user.speciality = speciality
    user.address = address
    user.email = email
    user.hashed_password = hashed_password
    session = db_session.create_session()
    session.add(user)
    session.commit()


@app.route("/add_user")
def add_user():
    add_user_func(surname="Scott", name="Ridley", age=21, position="captain",
                  speciality="research engineer", address="module_1", email="scott_chief@mars.org")
    add_user_func(surname="Maria", name="Zyryanova", age=15, position="coder",
                  speciality="engineer", address="module_1", email="m@x@_progy@mars.org")
    add_user_func(surname="Alex", name="Zyryanov", age=40, position="develop",
                  speciality="develop engineer", address="module_4", email="alex@mars.org")
    add_user_func(surname="Yulia", name="Zyryanova", age=18, position="medic",
                  speciality="врач", address="module_3", email="yuila@mars.org")
    return "4 пользователя добавлены в базу данных"


if __name__ == '__main__':
    main()
