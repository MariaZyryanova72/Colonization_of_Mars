import requests
from flask_restful import Api

from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_restful import Api
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.jobs import Jobs
from data.users import User
from data.departments import Department

import users_api
import jobs_api
import users_resource

from jobform import JobsForm
from departamenform import DepartamentsForm
from loginform import LoginForm
from registerform import RegisterForm
import jobs_resource

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars.sqlite")
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    app.register_blueprint(users_api.blueprint)
    app.register_blueprint(jobs_api.blueprint)
    app.run()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def add_user_func(name, city_from, surname=None, age=None, position=None, speciality=None,
                  address=None, email=None, hashed_password=None):
    new_user = User()
    new_user.surname = surname
    new_user.name = name
    new_user.age = age
    new_user.city_from = city_from
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


@app.route("/")
def works_log():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("works_log.html", jobs=jobs)


@app.route("/departament")
def departament_list():
    session = db_session.create_session()
    departaments = session.query(Department).all()
    return render_template("departament_log.html", departaments=departaments)


@app.route("/add_user")
def add_user():
    add_user_func(surname="Scott", name="Ridley", age=21, position="captain",
                  speciality="research engineer", address="module_1", email="scott_chief@mars.org", city_from="Тюмень")
    add_user_func(surname="Maria", name="Zyryanova", age=15, position="coder",
                  speciality="engineer", address="module_1", email="m@x@_progy@mars.org", city_from="Санкт-Петербург")
    add_user_func(surname="Alex", name="Zyryanov", age=40, position="develop",
                  speciality="develop engineer", address="module_4", email="alex@mars.org", city_from="Москва")
    add_user_func(surname="Yulia", name="Zyryanova", age=18, position="medic",
                  speciality="врач", address="module_3", email="yuila@mars.org", city_from="Тюмень")
    return "4 пользователя добавлены в базу данных"


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register Form',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Register Form',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.login.data,
            position=form.position.data,
            age=form.age.data,
            city_from=form.city_from.data,
            surname=form.surname.data,
            speciality=form.speciality.data,
            address=form.address.data,
            hashed_password=form.password.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return "ok"
    return render_template('register.html', title='Register Form', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/add_jobs',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.title.data
        jobs.team_leader = form.team_leader.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        jobs.hazard_category = form.hazard_category.data
        current_user.jobs.append(jobs)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('job.html', title='Add job',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/edit_jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            jobs = session.query(Jobs).filter(Jobs.id == id,
                                              ((Jobs.user == current_user) | (current_user.id == 1))).first()
            if jobs:
                form.title.data = jobs.job
                form.team_leader.data = jobs.team_leader
                form.work_size.data = jobs.work_size
                form.collaborators.data = jobs.collaborators
                form.is_finished.data = jobs.is_finished
                form.hazard_category.data = jobs.hazard_category
            else:
                return "Вы не капитан и не создатель, значит не имеете доступ к работе"
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            jobs = session.query(Jobs).filter(Jobs.id == id,
                                              ((Jobs.user == current_user) | (current_user.id == 1))).first()
            if jobs:
                jobs.title = form.title.data
                jobs.team_leader = form.team_leader.data
                jobs.work_size = form.work_size.data
                jobs.collaborators = form.collaborators.data
                jobs.is_finished = form.is_finished.data
                form.hazard_category = jobs.hazard_category.data

                session.commit()
                return redirect('/')
            else:
                return "Вы не капитан и не создатель, значит не имеете доступ к работе"
        else:
            abort(404)
    return render_template('job.html', title='Редактирование работы', form=form)


@app.route('/delete_jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_jobs(id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == id)

    if jobs:
        jobs = session.query(Jobs).filter(Jobs.id == id,
                                          ((Jobs.user == current_user) | (current_user.id == 1))).first()
        if jobs:
            session.delete(jobs)
            session.commit()
        else:
            return "Вы не капитан и не создатель, значит не имеете доступ к работе"
    else:
        abort(404)
    return redirect('/')


@app.route('/departament/edit_departament/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departament(id):
    form = DepartamentsForm()
    if request.method == "GET":
        session = db_session.create_session()
        departament = session.query(Department).filter(Department.id == id).first()
        if departament:
            departament = session.query(Department).filter(Department.id == id,
                                                           ((Department.user_chief == current_user) |
                                                            (current_user.id == 1))).first()
            if departament:
                form.title.data = departament.title
                form.chief.data = departament.chief
                form.members.data = departament.members
                form.email.data = departament.email
            else:
                return "Вы не капитан и не создатель, значит не имеете доступ к департаменту"
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        departament = session.query(Department).filter(Department.id == id).first()
        if departament:
            departament = session.query(Department).filter(Department.id == id,
                                                           ((Department.user_chief == current_user) |
                                                            (current_user.id == 1))).first()
            if departament:
                departament.title = form.title.data
                departament.chief = form.chief.data
                departament.members = form.members.data
                departament.email = form.email.data
                session.commit()
                return redirect('/departament')
            else:
                return "Вы не капитан и не создатель, значит не имеете доступ к департаменту"
        else:
            abort(404)
    return render_template('departament.html', title='Редактирование департамента', form=form)

  
@app.route('/departament/delete_departament/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_departament(id):
    session = db_session.create_session()
    departament = session.query(Department).filter(Department.id == id)

    if departament:
        departament = session.query(Department).filter(Department.id == id,
                                                       ((Department.user_chief == current_user) |
                                                        (current_user.id == 1))).first()
        if departament:
            session.delete(departament)
            session.commit()
        else:
            return "Вы не капитан и не создатель, значит не имеете доступ к департаменту"
    else:
        abort(404)
    return redirect('/departament')


@app.route('/departament/add_departament',  methods=['GET', 'POST'])
@login_required
def add_departament():
    form = DepartamentsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        departament = Department()
        departament.title = form.title.data
        departament.chief = form.chief.data
        departament.members = form.members.data
        departament.email = form.email.data
        current_user.user_department.append(departament)
        session.merge(current_user)
        session.commit()
        return redirect('/departament')
    return render_template('departament.html', title='Add Departament',
                           form=form)


@app.route('/users_show/<int:user_id>',  methods=['GET', 'POST'])
def users_show(user_id):
    response = requests.get("http://127.0.0.1:5000/api/users")
    if response:
        json_response = response.json()
        user = json_response["user"][user_id - 1]
        user_name = user["name"]
        user_surname = user["surname"]
        user_city = user["city_from"]
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": user_city,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            pass

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        longitude, lattitude = toponym["Point"]["pos"].split(" ")

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ",".join([longitude, lattitude]),
            "l": "sat",
            "spn": "0.05,0.05",
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        return render_template('city_from.html', image=response.url,
                               name=user_name, surname=user_surname, city=user_city)


if __name__ == '__main__':
    main()
