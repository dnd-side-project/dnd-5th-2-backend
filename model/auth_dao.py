from sqlalchemy import text


class AuthDao:
    def __init__(self, database):
        self.db = database

    # 이메일 중복 검사
    def check_email(self, user_info):
        return self.db.execute(text(
            """
            SELECT email FROM USERS
            WHERE email=:email
            """
        ), user_info).fetchone()

    # 회원가입 시
    def insert_user(self, new_user):
        return self.db.execute(
            text(
                """
                INSERT INTO USERS (email, username, gender, hashed_password)
                VALUES (:email, :username, :gender, :password)
                """
            ),
            new_user).lastrowid

    # 로그인 시 갖고 있는 해시 비번 같은지 확인, 비밀번호 찾기 시 기존 비밀번호 확인
    def get_password(self, email):
        return self.db.execute(text(
            """
            SELECT hashed_password
            FROM USERS
            WHERE email=:email
            """
        ), {'email': email}).fetchone()

    # 로그인 시 새로 발급된 시크릿 키 삽입
    def insert_new_secret_key(self, id, secret_key):
        return self.db.execute(text(
            """
            UPDATE USERS SET secret_key = ":secret_key"
            WHERE id=:id
            """
        ), {'id': id, 'secret_key': secret_key})

    def get_secret_key(self, id):
        return self.db.execute(text(
            """
            SELECT secret_key FROM USERS
            WHERE id=:id
            """
        ), {'id': id}).fetchone()


    # 비밀번호 찾기 시 이메일 확인
    def get_id(self, id):
        return self.db.execute(text(
            """
            SELECT id FROM USERS
            WHERE id=:id
            """
        ), {'id':id}).fetchone()

    # 비밀번호 찾기 시 발급받은 임시 비번 삽입
    def insert_temp_password(self, id, temp_password):
        return self.db.execute(text(
            """
            INSERT INTO TEMP_PW (user_id, temp_password)
            VALUES (
            (SELECT id FROM USERS 
            WHERE USERS.id=:id), :temp_password
            )
            """
        ), {'id': id, 'temp_password': temp_password})

    # 발급된 임시 비번 확인
    def get_temp_password(self, id):
        return self.db.execute(text(
            """
            SELECT temp_password FROM TEMP_PW
            WHERE (
                (SELECT id FROM USERS
                WHERE id=:id) = user_id
            )
            """
        ), {"id": id}).fetchone()

    # 새로운 비번 삽입
    def insert_new_password(self, id, hashed_password):
        return self.db.execute(text(
            """
            UPDATE USERS SET hashed_password = ":hashed_password"
            WHERE id=:id
            """
        ), {'id': id, 'hashed_password': hashed_password})