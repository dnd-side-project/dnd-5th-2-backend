from sqlalchemy import text


class AuthDao:
    def __init__(self, database):
        self.db = database

    # 회원가입 시
    def insert_user(self, new_user):
        return self.db.execute(
            text(
                """
                INSERT INTO USERS (email, username, gender, hashed_password)
                VALUES (:email, :username, :gender, :password)
                """
            ),
            new_user,
        ).lastrowid

    # 로그인 시 갖고 있는 해시 비번 같은지 확인, 비밀번호 찾기 시 기존 비밀번호 확인
    def get_password(self, email):
        return self.db.execute(
            text(
                """
            SELECT hashed_password
            FROM USERS
            WHERE email=:email
            """
            ),
            {"email": email},
        ).fetchone()

    # 로그인 시 새로 발급된 시크릿 키 삽입
    def insert_new_secret_key(self, id, secret_key):
        return self.db.execute(
            text(
                """
            UPDATE USERS SET secret_key = ":secret_key"
            WHERE id=:id
            """
            ),
            {"id": id, "secret_key": secret_key},
        )

    def get_secret_key(self, id):
        return self.db.execute(
            text(
                """
            SELECT secret_key FROM USERS
            WHERE id=:id
            """
            ),
            {"id": id},
        ).fetchone()

    # 비밀번호 찾기 시 이메일 확인
    def get_id(self, email):
        return self.db.execute(
            text(
                """
            SELECT id FROM USERS
            WHERE email=:email
            """
            ),
            {"email": email},
        ).fetchone()
