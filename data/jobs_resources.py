from flask import jsonify
from flask_restful import Resource, abort, reqparse
from . import db_session
from .jobs import Jobs
from .parsing import parser_jobs


class JobsResource(Resource):
    def get(self, user_id):
        abort_if_jobs_not_found(user_id)
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).get(user_id)
        return jsonify({"jobs": jobs.to_dict(
            only=('team_leader', 'job', 'work_size', 'content', "collaborators", "is_finished", "categories"))})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'users': [item.to_dict(
            only=('team_leader', 'job', 'work_size', 'content', "collaborators", "is_finished", "categories")) for item in
            jobs]})

    def post(self):
        args = parser_jobs.parse_args()
        db_sess = db_session.create_session()
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            content=args['content'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
            categories=args['categories']
        )
        db_sess.add(jobs)
        db_sess.commit()
        return jsonify({'id': jobs.id})

    def delete(self, id):
        abort_if_jobs_not_found(id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_jobs_not_found(id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(id)
    if not jobs:
        abort(404, message=f"Jobs {id} not found")
