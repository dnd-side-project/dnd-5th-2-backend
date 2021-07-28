from flask import Blueprint, request


def create_auth_blueprint(services):
    auth_service = services.auth_service

    auth_bp = Blueprint("user", __name__, url_prefix="/auth")

    @auth_bp.route("/signup", methods=["POST"])
    def signup():
        new_user = request.json
        auth_service.create_new_user(new_user)
        return "", 200

    return auth_bp
