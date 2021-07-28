from sqlalchemy import text


class AuthDao:
    def __init__(self, database):
        self.db = database

    def insert_user(self, new_user):
        return self.db.execute(
            text(
                """
                INSERT INTO USERS (email, username, hashed_password)
                VALUES (:email, :username, :hashed_password)
                """
            ),
            new_user,
        )
