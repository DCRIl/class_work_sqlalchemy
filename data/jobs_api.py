import flask

from flask import jsonify, request, make_response
from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=(
                    'team_leader', 'job', 'work_size', 'content', 'collaborators', 'start_date', 'end_date',
                    'is_finished',
                    'categories'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:id>')
def get_job(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=(
                    'team_leader', 'job', 'work_size', 'content', 'collaborators', 'start_date', 'end_date',
                    'is_finished',
                    'categories'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'content', "collaborators", "is_finished", "categories"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs()
    jobs.team_leader = request.json['team_leader']
    jobs.job = request.json['job']
    jobs.work_size = request.json['work_size']
    jobs.content = request.json['content']
    jobs.collaborators = request.json['collaborators']
    jobs.is_finished = request.json['is_finished']
    jobs.categories = request.json['categories']
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/<int:id>', methods=['POST'])
def edit_jobs(id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'content', "collaborators", "is_finished", "categories"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if jobs:
        jobs.team_leader = request.json['team_leader']
        jobs.job = request.json['job']
        jobs.work_size = request.json['work_size']
        jobs.content = request.json['content']
        jobs.collaborators = request.json['collaborators']
        jobs.is_finished = request.json['is_finished']
        jobs.categories = request.json['categories']
        db_sess.add(jobs)
        db_sess.commit()
    else:
        return make_response(jsonify({'error': 'Not Found'}), 404)
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})
