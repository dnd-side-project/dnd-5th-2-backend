import os

password = os.getenv("DB_PASSWORD")

DB = {
    "user": "root",
    "password": password,
    "host": "dnd-5th-2-db.ckxtrzia3cfx.ap-northeast-2.rds.amazonaws.com",
    "port": 3306,
    "database": "ggulgguk",
}

DB_URL = f"mysql+mysqlconnector://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset=utf8mb4&collation=utf8mb4_general_ci"


BUCKET = "dnd-5th-2"
MEDIA_URL = f"https://{BUCKET}.s3.amazonaws.com/"
PAGE_SIZE = 10
