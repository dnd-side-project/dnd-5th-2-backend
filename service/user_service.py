class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def get_user(self, user_name):
        user_info = self.user_dao.get_user(user_name)
        user_info = user_info._asdict()
        return user_info

    def edit_user(self, user_info):
        self.user_dao.delete_type(user_info)
        self.user_dao.edit_user(user_info)
        self.user_dao.edit_type(user_info)

    def get_other_user(self, username):
        other_user_info = self.user_dao.get_other_user(username)
        other_user_info = other_user_info._asdict()
        return other_user_info

    def get_wishlist(self, email):
        user_wishlist = self.user_dao.get_wishlist(email)
        if user_wishlist:
            wish_result = {}
            i = 0
            for item in user_wishlist:
                i += 1
                wish_dict = {}
                wish_dict["supplementId"] = item[0]
                wish_dict["supplementName"] = item[1]
                wish_dict["companyName"] = item[2]
                wish_dict["appearance"] = item[3]
                wish_dict["avgRating"] = item[4]
                wish_result[i] = wish_dict
            return wish_result
        else:
            return None

    def insert_wishlist(self, user_info):
        self.user_dao.insert_wishlist(
            user_info["email"], user_info["supplementId"])

    def delete_wishlist(self, user_info):
        self.user_dao.delete_wishlist(
            user_info["email"], user_info["supplementId"])

    def check_user_type(self, user_info):
        check_user_type = self.user_dao.check_user_type(user_info)
        if check_user_type:
            return check_user_type
        else:
            return None

    def delete_type(self, user_info):
        self.user_dao.delete_type(user_info)
    
    def insert_type(self, email, user_type):
        self.user_dao.insert_type(email, user_type)