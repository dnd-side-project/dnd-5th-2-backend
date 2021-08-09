import jwt
from functools import wraps

from flask import Blueprint, jsonify, request, Response, g


def create_reviews_blueprint(services):
    reviews_service = services.reviews_service
    auth_service = services.auth_service

    reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")

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
                if user_secret_key is None:
                    return Response(status=401)

                try:
                    payload = jwt.decode(access_token, user_secret_key, "HS256")
                except jwt.InvalidTokenError:
                    return Response(status=401)
                g.user_id = user_id

            else:
                return Response(status=401)

            return f(*args, **kwargs)

        return decorated_function

    @reviews_bp.route("", methods=["GET"])
    def review():
        get_args = request.args.get
        user_id = get_args("userId")
        supplement_id = get_args("supplementId")
        page = get_args("page")

        if user_id is not None and not user_id.isnumeric():
            return "잘못된 사용자 ID 입니다", 400
        if supplement_id is not None and not supplement_id.isnumeric():
            return "잘못된 영양제 ID 입니다", 400
        if page is not None and page.isnumeric() is False:
            return "잘못된 페이지 숫자 입니다", 400

        if user_id is not None:
            user_id = int(user_id)
        if supplement_id is not None:
            supplement_id = int(supplement_id)
        if page is not None:
            page = int(page)
        else:
            page = 1

        reviews = reviews_service.get_reviews(user_id, supplement_id, page)

        if reviews is None:
            return "리뷰가 존재하지 않습니다", 404
        return jsonify(reviews)

    @reviews_bp.route("", methods=["POST"])
    @login_required
    def create_review():
        user_id = g.user_id
        supplement_id = request.form.get("supplementId")
        review = reviews_service.get_review_id(user_id, supplement_id)
        if review is not None:
            return "리뷰가 이미 존재합니다", 409

        new_review = {}
        new_review["user_id"] = user_id
        new_review["supplement_id"] = supplement_id
        new_review["rating"] = request.form.get("rating")
        new_review["text"] = request.form.get("text")
        review_id = reviews_service.create_review(new_review)

        if "imgs" in request.files:
            review_imgs = request.files.getlist("imgs")
            reviews_service.upload_review_imgs(review_id, review_imgs)
        return "", 200

    @reviews_bp.route("", methods=["PUT"])
    @login_required
    def update_review():
        user_id = g.user_id
        supplement_id = request.form.get("supplementId")
        review = reviews_service.get_reviews(user_id, supplement_id)
        if review is None:
            return "존재하지 않는 리뷰입니다", 404

        new_review = {}
        new_review["user_id"] = user_id
        new_review["supplement_id"] = supplement_id
        new_review["rating"] = request.form.get("rating")
        new_review["text"] = request.form.get("text")
        reviews_service.update_review(new_review)

        if "imgs" in request.files:
            review = reviews_service.get_review_id(user_id, supplement_id)
            review_id = review[0]
            review_imgs = request.files.getlist("imgs")
            reviews_service.update_review_imgs(review_id, review_imgs)
        return "", 200

    @reviews_bp.route("", methods=["DELETE"])
    @login_required
    def delete_review():
        payload = request.json
        user_id = g.user_id
        supplement_id = payload["supplementId"]
        page = 1
        review = reviews_service.get_reviews(user_id, supplement_id, page)

        if review is None:
            return "존재하지 않는 리뷰입니다", 404

        reviews_service.delete_review(user_id, supplement_id)
        return "", 200

    return reviews_bp
