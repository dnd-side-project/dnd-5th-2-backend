import string
import secrets

from flask import Blueprint, request, jsonify


def create_auth_blueprint(services):
    auth_service = services.auth_service

    auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

    @auth_bp.route("/signup", methods=["POST"])
    def signup():
        new_user = request.json
        new_user_id = auth_service.create_new_user(new_user)
        return "", 200

    @auth_bp.route("/login", methods=["POST"])
    def login():
        user_info = request.json
        authorized = auth_service.login(user_info)

        if authorized:
            user_id = auth_service.check_id(user_info["email"])
            auth_service.insert_new_secret_key(user_id)
            secret_key = auth_service.get_secret_key(user_id)
            token = auth_service.generate_access_token(user_id, secret_key)

            return jsonify({"access_token": token})
        else:
            return "", 401

    return auth_bp
