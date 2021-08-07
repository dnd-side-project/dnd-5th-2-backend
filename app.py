import os

from flask import Flask
from sqlalchemy import create_engine
from dotenv import load_dotenv
import boto3

from model import AuthDao, SupplementsDao, UserDao, ReviewsDao
from service import AuthService, SupplementsService, UserService, ReviewsService
from view import create_endpoints


class Services:
    pass


def create_app(test_config=None):
    """앱 생성

    어플리케이션 팩토리 패턴으로 Flask 앱을 생성.
    Data Assess Object, Service, View로 구성된 3 티어 아키텍쳐 패턴 구현
    """
    # 환경 변수 설정
    load_dotenv()

    app = Flask(__name__)

    if test_config is None:
        app.config.from_envvar("APP_CONFIG_FILE")
    else:
        app.config.update(test_config)

    database = create_engine(app.config["DB_URL"], encoding="utf-8", max_overflow=0)
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=os.environ["S3_ACCESS_KEY"],
        aws_secret_access_key=os.environ["S3_SECRET_KEY"],
    )

    # Persistence 레이어
    auth_dao = AuthDao(database)
    supplements_dao = SupplementsDao(database)
    user_dao = UserDao(database)
    review_dao = ReviewsDao(database)

    # Business 레이어
    services = Services
    services.auth_service = AuthService(auth_dao, app.config)
    services.supplements_service = SupplementsService(supplements_dao)
    services.user_service = UserService(user_dao)
    services.reviews_service = ReviewsService(review_dao)

    # Presentation 레이어
    create_endpoints(app, services)

    return app
