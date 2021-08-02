DB = {
    "user": "root",
    "password": "RnfRjr123",
    "host": "localhost",
    "port": 3306,
    "database": "ggulgguk",
}

DB_URL = f"mysql+mysqlconnector://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset=utf8mb4&collation=utf8mb4_general_ci"

MEDIA_URL = f"/home/sangmin/github/dnd-5th-2-backend/media/"
