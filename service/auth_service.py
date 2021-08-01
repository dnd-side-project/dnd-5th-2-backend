import string
import secrets

import bcrypt
import jwt


class AuthService:
    def __init__(self, auth_dao, config):
        self.auth_dao = auth_dao
        self.config = config

    def create_new_user(self, new_user):
        new_user["password"] = bcrypt.hashpw(
            new_user["password"].encode("UTF-8"), bcrypt.gensalt()
        )
        new_user_id = self.auth_dao.insert_user(new_user)
        return new_user_id

    def login(self, user_info):
        email = user_info["email"]
        password = user_info["password"]
        user_private = self.auth_dao.get_password(email)
        authorized = user_private[0] and bcrypt.checkpw(
            password.encode("UTF-8"), user_private[0].encode("UTF-8")
        )
        return authorized

    def generate_access_token(self, id, secret_key):
        payload = {"user_id": id}
        token = jwt.encode(payload, secret_key, "HS256")
        return token

    def get_secret_key(self, id):
        secret_key = self.auth_dao.get_secret_key(id)
        return secret_key[0]

    # 로그인 시 새로 발급된 시크릿 키 삽입
    def insert_new_secret_key(self, id):
        string_pool = string.ascii_letters + string.digits
        while True:
            secret_key = "".join(secrets.choice(string_pool) for _ in range(10))
            if (
                any(c.islower() for c in secret_key)
                and any(c.isupper() for c in secret_key)
                and sum(c.isdigit() for c in secret_key) >= 3
            ):
                break
        return self.auth_dao.insert_new_secret_key(id, secret_key)

    # 비밀번호 찾기 시 id 확인, 토큰 생성 시 필요한 id
    def check_id(self, email):
        get_id = self.auth_dao.get_id(email)
        return get_id[0]
