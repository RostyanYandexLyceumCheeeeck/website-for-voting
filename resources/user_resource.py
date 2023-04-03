from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.users import User


def abort_if_user_not_found(email):
    session = db_session.create_session()
    user = session.query(User).get(email)
    if not user:
        abort(404, message=f"User {email} not found")
    return user


parser = reqparse.RequestParser()
parser.add_argument('id', required=True)
parser.add_argument('name', required=True)
parser.add_argument('created_date', required=True, type=str)
parser.add_argument('email', required=True, type=str)


class UserResource(Resource):
    def get(self, user_id: int):
        user = abort_if_user_not_found(user_id)
        print("YEP", user)
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'email', 'created_date'))})

    def delete(self, user_id):
        user = abort_if_user_not_found(user_id)
        session = db_session.create_session()
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):

    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('id', 'name', 'email', 'created_date')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            id=args['id'],
            name=args['name'],
            email=args['email'],
            created_date=args['created_date'],
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
