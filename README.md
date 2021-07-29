# dnd-5th-2-backend

DnD 5기 2조 백엔드 레포지토리

## 개발환경 설정

-   가상환경 생성 및 requriements 설치

```bash
$ python3 -m venv virtualenv
$ pip install -r requriements.txt
```

-   환경변수 설정
프로젝트 루트 디렉토리에 .env 파일 생성후 관리

```
FLASK_APP=app.py
FLASK_ENV=development
APP_CONFIG_FILE= development.py 설정파일 경로
```

-   데이터베이스 설정
데이터베이스 생성 후 sql 스크립트로 테이블 생성

```bash
$ mariadb -u root -p -e "create database ggulgguk default character set utf8";
$ mariadb -u root -p ggulgguk < database.sql
```

-   config 설정
/config/development.py 본인 환경에 맞게 수정

-   서버 실행

```bash
flask run
```
