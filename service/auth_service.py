import string
import secrets

import bcrypt
import jwt


class AuthService:
    def __init__(self, auth_dao, config):
        self.auth_dao = auth_dao
        self.config = config

    def check_email(self, user_info):
        email = self.auth_dao.check_email(user_info)
        if email:
            return email
        else:
            return None

    def check_username(self, user_info):
        username = self.auth_dao.check_username(user_info)
        if username:
            return username
        else:
            return None

    def create_new_user(self, new_user):
        new_user["password"] = bcrypt.hashpw(
            new_user["password"].encode("UTF-8"), bcrypt.gensalt()
        )
        new_user["password"] = new_user["password"].decode("utf-8")
        return self.auth_dao.insert_user(new_user)

    def login(self, user_info):
        email = user_info["email"]
        password = user_info["password"]
        user_password = self.auth_dao.get_password(email)

        authorized = user_password["hashed_password"] and bcrypt.checkpw(
            password.encode("UTF-8"), user_password["hashed_password"].encode("UTF-8")
        )
        return authorized

    def generate_access_token(self, user_id, secret_key):
        payload = {"user_id": user_id}
        token = jwt.encode(payload, secret_key, "HS256")
        return token

    def get_secret_key(self, user_id):
        user_secret_key = self.auth_dao.get_secret_key(user_id)
        if user_secret_key is None:
            return None
        return user_secret_key["secret_key"]

    # 로그인 시 새로 발급된 시크릿 키 삽입
    def insert_new_secret_key(self, user_id):
        string_pool = string.ascii_letters + string.digits
        while True:
            secret_key = "".join(secrets.choice(string_pool) for _ in range(10))
            if (
                any(c.islower() for c in secret_key)
                and any(c.isupper() for c in secret_key)
                and sum(c.isdigit() for c in secret_key) >= 3
            ):
                break
        self.auth_dao.insert_new_secret_key(user_id, secret_key)

    def check_id(self, email):
        user_id = self.auth_dao.get_id(email)
        return user_id["id"]

    def check_having_temp_password(self, user_id):
        temp_password = self.auth_dao.get_temp_password(user_id)
        if temp_password:
            return temp_password
        else:
            return None

    # 비밀번호 찾기 시 발급받은 임시 비번 삽입
    def insert_temp_password(self, email, temp_password):
        self.auth_dao.insert_temp_password(email, temp_password)

    # 발급된 임시 비번 확인
    def check_temp_password(self, user_id, user_temp_password):
        temp_password = self.auth_dao.get_temp_password(user_id)
        return user_temp_password == temp_password["temp_password"]

    def update_temp_password(self, email, temp_password):
        self.auth_dao.update_temp_password(email, temp_password)

    # 새로운 비번 삽입
    def insert_new_password(self, user_id, new_password):
        hashed_password = bcrypt.hashpw(new_password.encode("UTF-8"), bcrypt.gensalt())
        self.auth_dao.insert_new_password(user_id, hashed_password)
