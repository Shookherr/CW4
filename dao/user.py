from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def get_user(self, email):
        return self.session.query(User).filter(User.email == email).one_or_none()

    def get_user_by_name(self, name):
        return self.session.query(User).filter(User.name == name).first()

    def create(self, user_data):
        usr = User(**user_data)
        self.session.add(usr)
        self.session.commit()
        return usr

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_data):
        user = self.get_one(user_data.get("id"))
        # print(user_data.items())
        for key, val in user_data.items():
            # print(key, val)
            setattr(user, key, val)
        self.session.add(user)
        self.session.commit()
