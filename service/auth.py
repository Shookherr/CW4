import datetime
import calendar

import jwt

import constants
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def token_generate(self, email, pwd, is_refresh=False):  # генерация access и refresh токенов по email и паролю
        user = self.user_service.get_user(email)  # получение данных юзера из БД

        # Ошибка, если в БД нет юзера или не совпадают пароли запроса и БД
        if user is None or (not is_refresh and not self.user_service.passwords_compare(user.password, pwd)):
            raise Exception()

        data = {'email': user.email, }

        minutes = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # время жизни access токена
        data['exp'] = calendar.timegm(minutes.timetuple())
        # Генерация access токена
        access_token = jwt.encode(data, constants.TKN_SECRET, algorithm=constants.TKN_ALGO)

        days = datetime.datetime.utcnow() + datetime.timedelta(days=130)  # время жизни refresh токена
        data['exp'] = calendar.timegm(days.timetuple())
        # Генерация refresh токена
        refresh_token = jwt.encode(data, constants.TKN_SECRET, algorithm=constants.TKN_ALGO)

        # Возврат новых токенов
        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_token(self, refresh_token):  # генерация access и refresh токенов по refresh_token
        # Декодирование refresh токена из запроса
        data = jwt.decode(jwt=refresh_token, key=constants.TKN_SECRET, algorithms=[constants.TKN_ALGO])

        # Email пользователя из токена
        email = data.get('email')

        # Данные пользователя из БД по имени
        user = self.user_service.get_user(email)

        if user is None:
            raise Exception()

        # Генерация access и refresh токенов
        return self.token_generate(email, user.password, is_refresh=True)

    def validate_tokens(self, access_token, refresh_token):
        for token in [access_token, refresh_token]:
            try:
                jwt.decode(jwt=token, key=constants.TKN_SECRET, algorithms=[constants.TKN_ALGO])
            except Exception as e:
                # return f'Validate tokens failure: {e}'
                return False
        # return 'Validate tokens OK'
        return True
