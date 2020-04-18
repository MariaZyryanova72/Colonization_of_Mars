from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=bool)
parser.add_argument('city_from', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True, type=bool)
parser.add_argument('email', required=True, type=int)
parser.add_argument('hashed_password', required=True, type=int)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'city_from',
                  'speciality', 'address', 'email', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'city_from',
                  'speciality', 'address', 'email', 'hashed_password')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            city_from=args['city_from'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})
