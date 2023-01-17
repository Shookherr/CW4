from flask_restx import Resource, Namespace
from flask import request

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = user_service.get_all()
        return UserSchema(many=True).dump(rs), 200

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"users/{user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        rs = user_service.get_one(uid)
        return UserSchema().dump(rs), 200

    # def put(self, uid):

    def patch(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

    def delete(self, uid):
        user_service.delete(uid)
        return "", 204


@user_ns.route('/password')
class UpdateUserPasswordView(Resource):
    def put(self):
        req_json = request.json
        email = req_json.get('email')
        old_password = req_json.get('old_password')
        new_password = req_json.get('new_password')

        user = user_service.get_user(email)

        if user_service.passwords_compare(user.password, old_password):  # пароли совпали
            user.password = user_service.pwd_hashing(new_password)  # замена пароля с предварительным hash
            result = UserSchema().dump(user)
            user_service.update(result)     # изменение
            print('Password has been changed')
        else:
            print('Password not been changed')

        return '', 201
