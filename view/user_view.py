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

    @user_bp.route("/", methods=['GET'])
    @login_required
    def get_user():
        user_name = request.args.get("username")
        return user_service.get_user(user_name)

    @user_bp.route("", methods=['PUT'])
    @login_required
    def edit_user():
        user_info = request.json
        user_service.edit_user(user_info)
        return "", 200

    @user_bp.route("/<user_id>", methods=['GET'])
    def get_other_user(user_id):
        return user_service.get_other_user(user_id)

    @user_bp.route("/wishlist", methods=['GET'])
    @login_required
    def get_wishlist():
        user_id = request.args.get("user_id")
        return user_service.get_wishlist(user_id)

    @user_bp.route("/wishlist", methods=['POST'])
    @login_required
    def insert_wishlist():
        user_info = request.json
        user_service.insert_wishlist(user_info)
        return "", 200

    @user_bp.route("/wishlist", methods=['DELETE'])
    @login_required
    def delete_wishlist():
        user_info = request.json
        user_service.delete_wishlist(user_info["email"], user_info["supplementId"])
        return "", 200

    @user_bp.route("/type", methods=['POST'])
    @login_required
    def insert_type():
        user_info = request.json
        user_service.insert_type(user_info["email"], user_info["type"])
        return "", 200


    return user_bp