import bcrypt


class AuthService:
    def __init__(self, auth_dao, config):
        self.auth_dao = auth_dao
        self.config = config

    def create_new_user(self, new_user):
        new_user["hashed_password"] = bcrypt.hashpw(
            new_user["password"].encode("UTF-8"), bcrypt.gensalt()
        )

        new_user_id = self.auth_dao.insert_user(new_user)
        return new_user_id
