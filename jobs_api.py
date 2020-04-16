import flask
from flask import jsonify, request
from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs',  methods=['GET'])
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


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request1'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'] if 'work_size' in request.json else None,
        collaborators=request.json['collaborators'] if 'collaborators' in request.json else None,
        is_finished=request.json['is_finished'] if 'is_finished' in request.json else None
    )
    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})

