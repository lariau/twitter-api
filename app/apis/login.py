from flask_restplus import Namespace, Resource, fields
from flask import abort
from app.models import User
from app import db

api = Namespace('login')

json_user = api.model('User', {
    "username": fields.String,
    "email": fields.String
})


@api.route('<key>', methods=['POST'])
@api.response(404, 'Invalid key')
class LoginResource(Resource):
    @api.marshal_with(json_user, code=200)
    def post():
        key = api.payload["api_key"]
        user = db.session.query(User).where(api_key == key)
        if len(user.username) > 0:
            login_user(user)
        return user
