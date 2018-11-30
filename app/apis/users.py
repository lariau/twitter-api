from flask_restplus import Namespace, Resource, fields
from flask import abort
from app.models import User
from app import db

api = Namespace('users')

json_user = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'api_key': fields.String
})

json_new_user = api.model('New user', {
    'username': fields.String(required=True),
    'email': fields.String(required=True)
})

@api.route('')
class UserResource(Resource):
    @api.marshal_with(json_user, code=201)
    @api.expect(json_new_user, validate=True)
    @api.response(422, 'Invalid user')
    def post(self):
        username = api.payload["username"]
        email = api.payload["email"]
        if len(username) > 0 and len(email) > 0 :
            user = User(username=username,email=email)
            db.session.add(user)
            db.session.commit()
            return user, 201
        else:
            return abort(422, "Username and email must be provided")

    @api.marshal_list_with(json_new_user)
    def get(self):
        users = db.session.query(User).all()
        return users
