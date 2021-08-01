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
        if email is None:
            return True
        else:
            return False

    def create_new_user(self, new_user):
        new_user["password"] = bcrypt.hashpw(
            new_user["password"].encode("UTF-8"), bcrypt.gensalt()
        )
        new_user_id = self.auth_dao.insert_user(new_user)
        return new_user_id

    def login(self, user_info):
        email = user_info['email']
        password = user_info['password']
        user_private = self.auth_dao.get_password(email)
        print(user_private)

        authorized = user_private[0] and bcrypt.checkpw(
            password.encode('UTF-8'), user_private[0].encode('UTF-8'))
            
        print(authorized)
        return authorized

    def generate_access_token(self, id, secret_key):
        payload = {     
            'id': id
        }
        token = jwt.encode(payload, secret_key, 'HS256') 
        print(f'token={token}')
        return token

    def get_secret_key(self, id):
        secret_key =  self.auth_dao.get_secret_key(id)
        print(secret_key)
        return secret_key[0]

    # 로그인 시 새로 발급된 시크릿 키 삽입
    def insert_new_secret_key(self, id):
        string_pool = string.ascii_letters + string.digits
        while True:
            secret_key = ''.join(secrets.choice(string_pool) for _ in range(10))
            if (any(c.islower() for c in secret_key) 
                and any(c.isupper() for c in secret_key) 
                and sum(c.isdigit() for c in secret_key) >= 3):
                break
        print(secret_key)
        return self.auth_dao.insert_new_secret_key(id, secret_key)

    # 비밀번호 찾기 시 id 확인, 토큰 생성 시 필요한 id
    def check_id(self, id):
        get_id =  self.auth_dao.get_id(id)
        return get_id[0]      

    # 비밀번호 찾기 시 발급받은 임시 비번 삽입
    def insert_temp_password(self, id, temp_password):
        return self.auth_dao.insert_temp_password(id, temp_password)

    # 발급된 임시 비번 확인
    def check_temp_password(self, id, user_temp_password):
        temp_password = self.auth_dao.get_temp_password(id)
        return user_temp_password == temp_password['temp_password']
        
    # 새로운 비번 삽입
    def insert_new_password(self, id, new_password):
        hashed_password = bcrypt.hashpw(
            new_password.encode("UTF-8"), bcrypt.gensalt()
        )
        return self.auth_dao.insert_new_password(id, hashed_password)



