from sqlalchemy import text
from flask import current_app


class SupplementsDao:
    def __init__(self, database):
        self.db = database

    def get(self, supplement_id):
        return self.db.execute(
            text(
                """
                SELECT * 
                FROM SUPPLEMENTS
                WHERE id = :supplement_id
                """
            ),
            {"supplement_id": supplement_id},
        ).fetchone()

    def search_by_name(self, supplement_name, page_size, page):
        return self.db.execute(
            text(
                """
                SELECT *
                FROM SUPPLEMENTS
                WHERE supplement_name LIKE :supplement_name
                LIMIT :page_size OFFSET :page
                """
            ),
            {
                "supplement_name": "%" + supplement_name + "%",
                "page_size": page_size,
                "page": page,
            },
        ).fetchall()

    def search_by_tag(self, tag, page_size, page):
        return self.db.execute(
            text(
                """
                SELECT *
                FROM SUPPLEMENTS
                LEFT JOIN SUPPLEMENT_TAGS 
                ON SUPPLEMENTS.id = SUPPLEMENT_TAGS.supplement_id
                WHERE SUPPLEMENT_TAGS.tag_name = :tag
                LIMIT :page_size OFFSET :page
                """
            ),
            {
                "tag": tag,
                "page_size": page_size,
                "page": page,
            },
        ).fetchall()

    def search_by_tags(self, tags, page_size, page):
        tags_string = ""
        for i in range(len(tags)):
            tags_string += '"' + tags[i] + '"'
            if i == len(tags) - 1:
                break
            tags_string += ", "

        return self.db.execute(
            text(
                """
                SELECT *
                FROM SUPPLEMENTS
                LEFT JOIN SUPPLEMENT_TAGS 
                ON SUPPLEMENTS.id = SUPPLEMENT_TAGS.supplement_id
                WHERE SUPPLEMENT_TAGS.tag_name IN (
                """
                + tags_string
                + ")"
                + """
                LIMIT :page_size OFFSET :page
                """
            ),
            {
                "page_size": page_size,
                "page": page,
            },
        ).fetchall()

    def get_type_tags(self, type):
        return self.db.execute(
            text(
                """
                SELECT tag_name
                FROM TYPE_TAG
                RIGHT JOIN TYPES
                ON TYPE_TAG.type_name = TYPES.name
                WHERE type_name = :type
                """
            ),
            {"type": type},
        ).fetchall()

    def get_type(self, type):
        return self.db.execute(
            text(
                """
                SELECT *
                FROM TYPES
                WHERE name = :type
                """
            ),
            {"type": type},
        ).fetchone()

    def get_tag(self, tag):
        return self.db.execute(
            text(
                """
                SELECT *
                FROM TAGS
                WHERE name = :tag
                """
            ),
            {"tag": tag},
        ).fetchone()
