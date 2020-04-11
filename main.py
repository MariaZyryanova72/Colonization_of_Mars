from flask import Flask
from data import db_session
from data.jobs import Jobs
from data.users import User
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars.sqlite")
    app.run()


def add_user_func(name, surname=None, age=None, position=None, speciality=None,
                  address=None, email=None, hashed_password=None):
    new_user = User()
    new_user.surname = surname
    new_user.name = name
    new_user.age = age
    new_user.position = position
    new_user.speciality = speciality
    new_user.address = address
    new_user.email = email
    new_user.hashed_password = hashed_password
    session = db_session.create_session()
    session.add(new_user)
    session.commit()


def add_job_func(team_leader, job, work_size=None, collaborators=None, start_date=None,
                 end_date=None, is_finished=None):
    session = db_session.create_session()
    new_job = Jobs()
    new_job.team_leader = team_leader
    new_job.job = job
    new_job.work_size = work_size
    new_job.collaborators = collaborators
    new_job.start_date = start_date
    new_job.end_date = end_date
    new_job.is_finished = is_finished
    session.add(new_job)
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


@app.route("/add_job")
def add_job():
    add_job_func(team_leader=1, job="deployment of residential modules 1 and 2", work_size=15,
                 collaborators="2, 3", start_date=datetime.datetime.now(), is_finished=False)
    return "Добавлены в базу данных данные о работе"


if __name__ == '__main__':
    main()
