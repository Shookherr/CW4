from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service, user_service

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthService(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email')
        pwd_req = req_json.get('password')

        if None in [email, pwd_req]:
            return 'Email or password is missing.', 401

        return auth_service.token_generate(email, pwd_req), 201

    def put(self):
        req_json = request.json
        access_token = req_json.get('access_token')    # токен из запроса
        refresh_token = req_json.get('refresh_token')  # токен из запроса
        is_valid_tokens = auth_service.validate_tokens(access_token, refresh_token)  # проверка токенов
        if is_valid_tokens:
            return auth_service.approve_refresh_token(refresh_token), 201
        else:
            return 'Validate tokens failure', 403


@auth_ns.route('/register')
class RegisterUser(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email')
        pwd_req = req_json.get('password')

        if None in [email, pwd_req]:
            return 'Email or password is missing.', 401

        user_service.create(req_json)  # создание юзверя согласно запросу
        return '', 201
