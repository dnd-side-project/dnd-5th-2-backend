class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def get_user(self, user_name):
        return self.user_dao.get_user(user_name)

    def edit_user(self, user_info):
        # self.user_dao.insert_type("유형1")
        # self.user_dao.insert_type("유형2")

        self.user_dao.delete_type(user_info)
        self.user_dao.edit_user(user_info)
        self.user_dao.edit_type(user_info)

    def get_other_user(self, user_id):
        return self.user_dao.get_other_user(user_id)

    def get_wishlist(self, user_id):
        return self.user_dao.get_wishlist(user_id)

    def insert_wishlist(self, user_info):
        # self.user_dao.insert_supplement_id("1", "영양제")
        return self.user_dao.insert_wishlist(
            user_info["email"], user_info["supplementId"])

    def delete_wishlist(self, email, supplement_id):
        return self.user_dao.delete_wishlist(email, supplement_id)

    def check_user_type(self, email):
        if self.user_dao.check_user_type(email):
            return True
        else:
            return False

    def delete_type(self, email, type):
        return self.user_dao.delete_type(email, type)
    
    def insert_type(self, email, type):
        return self.user_dao.insert_type(email, type)