from sqlalchemy import text


class UserDao:
    def __init__(self, database):
        self.db = database

    def get_user(self, user_name):
        return self.db.execute(text(
            """
            SELECT username, email, gender, USER_TYPE.type_name
            FROM USERS
            LEFT OUTER JOIN USER_TYPE
            ON USERS.id = USER_TYPE.user_id
            WHERE USERS.username=:user_name
            """
        ), {'user_name': user_name}).fetchone()

    def delete_type(self, user_info):
        self.db.execute(text(
            """
            DELETE FROM USER_TYPE
            WHERE (
                (SELECT id FROM USERS
                WHERE email=:email) = user_id
            )
            """
        ), user_info)

    def edit_user(self, user_info):
        self.db.execute(text(
            """
            UPDATE USERS 
            SET username=:username, gender=:gender
            WHERE email=:email
            """
        ), user_info)

    def edit_type(self, user_info):
        self.db.execute(text(
            """
            INSERT INTO USER_TYPE (user_id, type_name) 
            VALUES (
                (SELECT id FROM USERS
                WHERE email=:email), :type
            )
            """
        ), user_info)

    def get_other_user(self, username):
        return self.db.execute(text(
            """
            SELECT username, USER_TYPE.type_name
            FROM USERS
            LEFT OUTER JOIN USER_TYPE
            ON USERS.id = USER_TYPE.user_id
            WHERE USERS.username=:username
            """
        ), {'username': username}).fetchone()

    ################ 위시리스트 ################
    def get_wishlist(self, email):
        return self.db.execute(text(
            """
            SELECT w.supplement_id, s.supplement_name, 
                s.company_name, s.appearance, s.avg_rating
            FROM 
                USERS AS u RIGHT OUTER JOIN WISHLIST AS w
                    ON u.id = w.user_id
                LEFT OUTER JOIN SUPPLEMENTS AS s
                    ON s.id = w.supplement_id
            WHERE u.email=:email
            """
        ), {'email': email}).fetchall()

    def insert_wishlist(self, email, supplement_id):
        self.db.execute(text(
            """
            INSERT INTO WISHLIST (user_id, supplement_id)
            VALUES (
                (SELECT id FROM USERS
                WHERE email=:email), :supplement_id
            )
            """
        ), {'email': email, 'supplement_id': supplement_id})

    def delete_wishlist(self, email, supplement_id):
        self.db.execute(text(
            """
            DELETE FROM WISHLIST 
            WHERE (user_id=(SELECT id FROM USERS WHERE email=:email)
                AND supplement_id=:supplement_id
            )
            """
        ), {'email': email, 'supplement_id': supplement_id})

    ################ 유형 #################
    def check_user_type(self, user_info):
        return self.db.execute(text(
            """
            SELECT user_id FROM USER_TYPE
            WHERE (
                (SELECT id FROM USERS
                WHERE email=:email) = user_id
            )
            """
        ), user_info).fetchone()

    def delete_type(self, user_info):
        self.db.execute(text(
            """
            DELETE FROM USER_TYPE
            WHERE (
                (SELECT id FROM USERS
                WHERE email=:email) = user_id
            )
            """
        ), user_info)

    def edit_user(self, user_info):
        self.db.execute(text(
            """
            UPDATE USERS
            SET username=:username, gender=:gender
            WHERE email=:email
            """
        ), user_info)

    def edit_type(self, user_info):
        self.db.execute(text(
            """
            INSERT INTO USER_TYPE (user_id, type_name) 
            VALUES (
                (SELECT id FROM USERS
                WHERE email=:email), :type
            )
            """
        ), user_info)

    def insert_type(self, email, user_type):
        self.db.execute(text(
            """
            INSERT INTO USER_TYPE (user_id, type_name)
            VALUES (
                (SELECT id FROM USERS
                WHERE email=:email), :user_type
            );
            """
        ), {'email': email,'user_type': user_type})
