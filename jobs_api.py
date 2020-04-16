import flask
from flask import jsonify
from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'news':
                [job.to_dict(only=('team_leader', 'job', 'work_size',
                                   'collaborators', 'start_date', 'end_date',
                                   'is_finished', 'user.name'))
                 for job in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>',  methods=['GET'])
def get_one_jobs(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'news': jobs.to_dict(only=('team_leader', 'job', 'work_size',
                                       'collaborators', 'start_date', 'end_date',
                                       'is_finished', 'user.name'))
        }
    )

