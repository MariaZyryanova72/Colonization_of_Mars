import flask
from flask import jsonify, request
from data import db_session
from data.users import User

blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users',  methods=['GET'])
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'user':
                [user.to_dict(only=('surname', 'name', 'age',
                                    'position', 'speciality', 'address',
                                    'email', 'hashed_password', 'modified_date'))
                 for user in users]
        }
    )


@blueprint.route('/api/users/<int:users_id>',  methods=['GET'])
def get_one_users(users_id):
    session = db_session.create_session()
    user = session.query(User).get(users_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('surname', 'name', 'age',
                                       'position', 'speciality', 'address',
                                       'email', 'hashed_password', 'modified_date'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif 'name' not in request.json:
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    user = User(
        surname=request.json['surname'] if 'surname' in request.json else None,
        name=request.json['name'],
        age=request.json['age'] if 'age' in request.json else None,
        position=request.json['position'] if 'position' in request.json else None,
        speciality=request.json['speciality'] if 'speciality' in request.json else None,
        address=request.json['address'] if 'address' in request.json else None,
        email=request.json['email'] if 'email' in request.json else None,
        hashed_password=request.json['hashed_password'] if 'hashed_password' in request.json else None,
    )
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    session = db_session.create_session()
    user = session.query(User).get(users_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['POST'])
def edit_users(users_id):
    session = db_session.create_session()
    user = session.query(User).get(users_id)
    if not user:
        return jsonify({'error': 'Not found'})
    user.surname = request.json['surname'] if 'surname' in request.json else user.surname
    user.name = request.json['name'] if 'name' in request.json else user.name
    user.age = request.json['age'] if 'age' in request.json else user.age
    user.position = request.json['position'] if 'position' in request.json else user.position
    user.speciality = request.json['speciality'] if 'speciality' in request.json else user.speciality
    user.address = request.json['address'] if 'address' in request.json else user.address
    user.email = request.json['email'] if 'email' in request.json else user.email
    user.hashed_password = request.json['hashed_password'] if 'hashed_password' in request.json \
        else user.hashed_password
    session.commit()
    return jsonify({'success': 'OK'})
