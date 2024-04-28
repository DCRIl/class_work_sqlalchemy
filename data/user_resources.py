from flask import jsonify
from flask_restful import Resource, abort, reqparse
from . import db_session
from .users import User
from .parsing import parser


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        return jsonify({"user": user.to_dict(
            only=("surname", "name", "age", "position", "speciality", "address", "email", "city_from"))})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=("surname", "name", "age", "position", "speciality", "address", "email", "city_from")) for item in
            users]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            city_from=args['city_from']
        )
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'id': user.id})

    def delete(self, id):
        abort_if_user_not_found(id)
        session = db_session.create_session()
        user = session.query(User).get(id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")
