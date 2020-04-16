import flask
from flask import jsonify
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
