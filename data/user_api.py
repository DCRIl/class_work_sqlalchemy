import flask

from flask import jsonify, request, make_response
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=("surname", "name", "age", "position", "speciality", "address", "email"))
                 for item in users]
        }
    )


@blueprint.route('/api/user/<int:id>')
def get_user(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == id).first()
    return jsonify(
        {
            'users':
                [item.to_dict(only=("surname", "name", "age", "position", "speciality", "address", "email"))
                 for item in users]
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ["surname", "name", "age", "position", "speciality", "address", "email"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    users = User()
    users.surname = request.json['surname']
    users.name = request.json['name']
    users.age = request.json['age']
    users.position = request.json['position']
    users.speciality = request.json['speciality']
    users.address = request.json['address']
    users.email = request.json['email']
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'id': users.id})


@blueprint.route('/api/user/<int:id>', methods=['POST'])
def edit_user(id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ["surname", "name", "age", "position", "speciality", "address", "email", "city_from"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == id).first()
    if users:
        users.surname = request.json['surname']
        users.name = request.json['name']
        users.age = request.json['age']
        users.position = request.json['position']
        users.speciality = request.json['speciality']
        users.address = request.json['address']
        users.email = request.json['email']
        users.city_from = request.json['city_from']
        db_sess.add(users)
        db_sess.commit()
    else:
        return make_response(jsonify({'error': 'Not Found'}), 404)
    return jsonify({'id': users.id})


@blueprint.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})
