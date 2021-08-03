import string
import secrets
from functools import wraps

from flask import Blueprint, request, jsonify, Response, g
import jwt


def create_auth_blueprint(services):
    auth_service = services.auth_service

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

    @auth_bp.route("/signup", methods=["POST"])
    def signup():
        new_user = request.json
        if auth_service.check_email(new_user) is not None:
            return jsonify({'message': "이메일이 존재합니다."})
        else:
            if auth_service.check_username(new_user) is not None:
                return jsonify({'message': "중복된 닉네임입니다."})
            else:
                auth_service.create_new_user(new_user)
                return "", 200

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

                return jsonify({
                    'access_token': token
                })
            else:
                return "", 401
        else:
            return jsonify({"message": "존재하지 않는 이메일 입니다."})
            


    @auth_bp.route("/generate-tmp-password", methods=['POST'])
    @login_required
    def generate_tmp_pw():
        email = request.json["email"]

        various_s = string.ascii_letters + string.digits
        while True:
            temp_password = ''.join(secrets.choice(various_s) for _ in range(10))

            if (any(c.islower() for c in temp_password) 
                and any(c.isupper() for c in temp_password) 
                and sum(c.isdigit() for c in temp_password) >= 3):
                break
        
        if auth_service.check_having_temp_password(email) is not None:
            auth_service.update_temp_password(email, temp_password)
        else:
            auth_service.insert_temp_password(email, temp_password)
        
        return jsonify({'temp_password': temp_password})


    @auth_bp.route("/reset-password", methods=['POST'])
    @login_required
    def reset_password():
        user_info = request.json

        # 발급된 임시 비번 확인
        if auth_service.check_temp_password(user_info["email"], user_info["tmpPassword"]):
            auth_service.insert_new_password(user_info["email"], user_info["newPassword"])
            return "", 200
        else:
            return jsonify({'message': '임시 비밀번호가 틀렸습니다.'})

    return auth_bp




    
