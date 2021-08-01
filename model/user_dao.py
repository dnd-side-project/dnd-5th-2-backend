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

    # def insert_type(self, type):
    #     self.db.execute(text(
    #         """
    #         INSERT INTO TYPES (name)
    #         VALUES (:type)
    #         """
    #     ), {'type': type})

    def delete_type(self, user_info):
        self.db.execute(text(
            """
            DELETE FROM USER_TYPE
            WHERE user_id=:id
            """
        ), user_info)

    def edit_user(self, user_info):
        self.db.execute(text(
            """
            UPDATE USERS 
            SET username=:username, email=:email, gender=:gender
            WHERE id=:id
            """
        ), user_info)

    def edit_type(self, user_info):
        self.db.execute(text(
            """
            INSERT INTO USER_TYPE (user_id, type_name) 
            VALUES (:id, :type)
            """
        ), user_info)

    def get_other_user(self, user_id):
        return self.db.execute(text(
            """
            SELECT username, USER_TYPE.type_name
            FROM USERS
            LEFT OUTER JOIN USER_TYPE
            ON USERS.id = USER_TYPE.user_id
            WHERE USERS.id=:user_id
            """
        ), {'user_id': user_id}).fetchone()

    ################ 위시리스트 ################

    # 무조건 user_id가 매개변수여야 함
    def get_wishlist(self, user_id):
        return self.db.execute(text(
            """
            SELECT s.supplement_name, w.supplement_id
            FROM 
                SUPPLEMENTS AS s LEFT OUTER JOIN WISHLIST AS w
                    ON s.id = w.supplement_id
                LEFT OUTER JOIN USERS AS u
                    ON w.user_id = u.id
            WHERE u.id=:user_id
            """
        ), {'user_id': user_id}).fetchall()

    # def insert_supplement_id(self, supplement_id, supplement):
    #     self.db.execute(text(
    #         """
    #         INSERT INTO SUPPLEMENTS (id, product_name)
    #         VALUES (:supplement_id, :supplement)
    #         """
    #     ), {'id': supplement_id, 'supplement': supplement})

    def insert_wishlist(self, email, supplement_id):
        return self.db.execute(text(
            """
            INSERT INTO WISHLIST (user_id, supplement_id)
            VALUES (
                (SELECT id FROM USERS
                WHERE email=:email), :supplement_id
            )
            """
        ), {'email': email, 'supplement_id': supplement_id})

    def delete_wishlist(self, email, supplement_id):
        return self.db.execute(text(
            """
            DELETE FROM WISHLIST 
            WHERE (user_id=(SELECT id FROM USERS WHERE email=:email)
                AND supplement_id=:supplement_id
            )
            """
        ), {'email': email, 'supplement_id': supplement_id})

    ############# 유형 ###############
    def insert_type(self, email, type):
        return self.db.execute(text(
            """
            INSERT INTO USER_TYPE (user_id, type_name)
            VALUES (
                (SELECT id FROM USERS
                WHERE email=:email), :type
            );
            """
        ), {'email': email, 'type': type})
