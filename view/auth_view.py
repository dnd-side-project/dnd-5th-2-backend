import string
import secrets
from functools import wraps

from flask import Blueprint, request, jsonify, Response, g
import jwt

from .utils import send_mail


def create_auth_blueprint(services):
    auth_service = services.auth_service
    user_service = services.user_service

    auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

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

    @auth_bp.route("/signup-email", methods=["POST"])
    def signup_email():
        new_user = request.json
        if auth_service.check_email(new_user) is not None:
            return jsonify({"exists": True})
        else:
            return jsonify({"exists": False})

    @auth_bp.route("/signup-username", methods=["POST"])
    def signup_user_name():
        new_user = request.json
        if auth_service.check_username(new_user) is not None:
            return jsonify({"exists": True})
        else:
            return jsonify({"exists": False})

    @auth_bp.route("/signup", methods=["POST"])
    def signup():
        new_user = request.json
        auth_service.create_new_user(new_user)
        return jsonify({"message": "회원가입 되었습니다."})
        
    @auth_bp.route("/login", methods=['POST'])
    def login():
        user_info = request.json
        if auth_service.check_email(user_info) is not None:
            authorized = auth_service.login(user_info)

            if authorized:
                user_id = auth_service.check_id(user_info['email'])
                auth_service.insert_new_secret_key(user_id)
                secret_key = auth_service.get_secret_key(user_id)
                token = auth_service.generate_access_token(
                    user_id, secret_key)

                user_info = user_service.get_user(user_id)

                return jsonify({"user": user_info,"token": token})
            else:
                return jsonify({"message": "비밀번호가 틀렸습니다."}), 403
        else:
            return jsonify({"message": "존재하지 않는 이메일 입니다."}), 404
            


    @auth_bp.route("/generate-tmp-password", methods=['POST'])
    @login_required
    def generate_tmp_pw():
        email = request.json["email"]
        user_id = g.user_id

        various_s = string.ascii_letters + string.digits
        while True:
            temp_password = ''.join(secrets.choice(various_s) for _ in range(10))

            if (any(c.islower() for c in temp_password) 
                and any(c.isupper() for c in temp_password) 
                and sum(c.isdigit() for c in temp_password) >= 3):
                break
        
        if auth_service.check_having_temp_password(user_id) is not None:
            auth_service.update_temp_password(email, temp_password)
        else:
            auth_service.insert_temp_password(email, temp_password)
        
        send_mail(email, temp_password)
        return jsonify({"message": "임시 비밀번호가 전송되었습니다."})


    @auth_bp.route("/reset-password", methods=['POST'])
    @login_required
    def reset_password():
        user_info = request.json
        user_id = g.user_id
        
        # 발급된 임시 비번 확인
        if auth_service.check_temp_password(user_id, user_info["tmp_password"]):
            auth_service.insert_new_password(user_id, user_info["new_password"])
            return jsonify({"message": "비밀번호가 변경되었습니다."})
        else:
            return jsonify({"message": "임시 비밀번호가 틀렸습니다."}), 403

    return auth_bp




    
