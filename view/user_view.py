from functools import wraps
from flask import Blueprint, request, jsonify, Response, g
import jwt


def create_user_blueprint(services):
    user_service = services.user_service
    auth_service = services.auth_service

    user_bp = Blueprint("user", __name__, url_prefix="/user")

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            access_token = request.headers.get("Authorization")
            if access_token:
                access_token = access_token.replace("Bearer ", "")
                try:
                    payload = jwt.decode(
                        access_token,
                        algorithms="HS256",
                        options={"verify_signature": False},
                    )
                except jwt.DecodeError:
                    return Response(status=401)
                user_id = payload["user_id"]
                user_secret_key = auth_service.get_secret_key(user_id)
                try:
                    payload = jwt.decode(access_token, user_secret_key, "HS256")
                except jwt.InvalidTokenError:
                    return Response(status=401)
                g.user_id = user_id
            else:
                return Response(status=401)
            return f(*args, **kwargs)

        return decorated_function

    @user_bp.route("/", methods=["GET"])
    @login_required
    def get_user():
        user_id = g.user_id
        return user_service.get_user(user_id)

    @user_bp.route("", methods=["PUT"])
    @login_required
    def edit_user():
        user_info = request.json
        if auth_service.check_username(user_info) is not None:
            return jsonify({"message": "중복된 닉네임입니다."})
        else:
            user_service.edit_user(user_info)
            return jsonify({"message": "정보가 수정되었습니다."})

    @user_bp.route("/<username>", methods=["GET"])
    def get_other_user(username):
        return user_service.get_other_user(username)

    @user_bp.route("/wishlist", methods=["GET"])
    @login_required
    def get_wishlist():
        user_id = g.user_id
        user_wishlist = user_service.get_wishlist(user_id)
        if user_wishlist is not None:
            return user_wishlist
        else:
            return jsonify({"messsage": "찜한 상품이 없습니다."})


    @user_bp.route("/wishlist", methods=["POST"])
    @login_required
    def insert_wishlist():
        user_info = request.json
        user_id = g.user_id
        user_service.insert_wishlist(user_id,user_info["supplementId"])
        return jsonify({"message": "영양제가 추가되었습니다."})

    @user_bp.route("/wishlist", methods=["DELETE"])
    @login_required
    def delete_wishlist():
        user_info = request.json
        user_id = g.user_id
        user_service.delete_wishlist(user_id, user_info["supplementId"])
        return jsonify({"message": "삭제되었습니다."})

    @user_bp.route("/type", methods=["POST"])
    @login_required
    def insert_type():
        user_info = request.json
        user_id = g.user_id
        if user_service.check_user_type(user_id) is not None:
            user_service.delete_type(user_id)
        type_list = user_info["type"].split(",")
        for user_type in type_list:
            user_service.insert_type(user_id, user_type)

        user_info = user_service.get_user(user_id)
        return user_info

    return user_bp
