class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def get_user(self, user_id):
        user_info = self.user_dao.get_user(user_id)
        # [('지현', 'jhiya7420@naver.com', '여성', 20, '간 건강'), ('지현', 'jhiya7420@naver.com', '여성', 20, '위 건강')]

        user_result = {}
        i = 0
        for item in user_info:
            if i < 1:
                user_result["user_name"] = item[0]
                user_result["email"] = item[1]
                user_result["gender"] = item[2]
                user_result["age"] = item[3]
                user_result["type_name"] = [item[4]]
            else:
                user_result["type_name"] += [item[4]]
            i += 1
            
        return user_result

    def edit_user(self, user_info):
        self.user_dao.edit_user(user_info)

    def get_other_user(self, username):
        other_user_info = self.user_dao.get_other_user(username)
        other_user_info = other_user_info._asdict()
        return other_user_info

    def get_wishlist(self, user_id):
        user_wishlist = self.user_dao.get_wishlist(user_id)
        if user_wishlist:
            wish_result = {}
            i = 0
            for item in user_wishlist:
                i += 1
                wish_dict = {}
                wish_dict["supplement_id"] = item[0]
                wish_dict["supplement_name"] = item[1]
                wish_dict["company_name"] = item[2]
                wish_dict["appearance"] = item[3]
                wish_dict["avg_rating"] = item[4]
                wish_result[i] = wish_dict
            return wish_result
        else:
            return None

    def insert_wishlist(self, user_id, supplement_id):
        self.user_dao.insert_wishlist(
            user_id, supplement_id)

    def delete_wishlist(self, user_id, supplement_id):
        self.user_dao.delete_wishlist(
            user_id, supplement_id)

    def check_user_type(self, user_id):
        check_user_type = self.user_dao.check_user_type(user_id)
        if check_user_type:
            return check_user_type
        else:
            return None

    def delete_type(self, user_id):
        self.user_dao.delete_type(user_id)
    
    def insert_type(self, user_id, user_type):
        self.user_dao.insert_type(user_id, user_type)