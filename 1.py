from data import db_session
from data.jobs import Jobs
from data.users import User
from data.departments import Department


db_session.global_init(input())
session = db_session.create_session()
dict_user = dict()
department = session.query(Department).filter(Department.id == 1).first()
users_department = [int(id) for id in department.members.split(", ")]

for job in session.query(Jobs).all():
    for user_id in [int(id) for id in job.collaborators .split(", ")]:
        dict_user[user_id] = dict_user.get(user_id, 0) + job.work_size
for user in session.query(User).filter(User.id.in_(users_department)).all():
    if dict_user.get(user.id, 0) > 25:
        print(f'{user.surname} {user.name}')
