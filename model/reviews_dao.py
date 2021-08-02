from sqlalchemy import text
from flask import current_app


class ReviewsDao:
    def __init__(self, database):
        self.db = database

    def get_review_id(self, user_id, supplement_id):
        return self.db.execute(
            text(
                """
                SELECT id
                FROM REVIEWS
                WHERE user_id = :user_id AND supplement_id = :supplement_id
                """
            ),
            {"user_id": user_id, "supplement_id": supplement_id},
        ).fetchone()

    def get_review(self, user_id, supplement_id):
        return self.db.execute(
            text(
                """
                    SELECT *
                    FROM REVIEWS
                    WHERE user_id = :user_id AND supplement_id = :supplement_id
                    """
            ),
            {"user_id": user_id, "supplement_id": supplement_id},
        ).fetchone()

    def get_reviews_by_user_id(self, user_id, page):
        return self.db.execute(
            text(
                """
                    SELECT *
                    FROM REVIEWS
                    WHERE user_id = :user_id 
                    LIMIT :PAGE_SIZE OFFSET :page
                    """
            ),
            {
                "user_id": user_id,
                "PAGE_SIZE": current_app.config["PAGE_SIZE"],
                "page": page,
            },
        ).fetchall()

    def get_reviews_by_supplement_id(self, supplement_id, page):
        return self.db.execute(
            text(
                """
                 SELECT *
                FROM REVIEWS
                WHERE supplement_id = :supplement_id
                LIMIT :PAGE_SIZE OFFSET :page
                """
            ),
            {
                "supplement_id": supplement_id,
                "PAGE_SIZE": current_app.config["PAGE_SIZE"],
                "page": page,
            },
        ).fetchall()

    def get_review_imgs(self, review_id):
        return self.db.execute(
            text(
                """
                SELECT img_url
                FROM REVIEW_IMGS
                WHERE review_id = :review_id
                """
            ),
            {"review_id": review_id},
        ).fetchall()

    def insert_review(self, new_review):
        return self.db.execute(
            text(
                """
                INSERT INTO REVIEWS (user_id, supplement_id, rating, text, registration_day)
                VALUES (:user_id, :supplement_id, :rating, :text, :registration_day)
                """
            ),
            new_review,
        ).lastrowid

    def update_review(self, new_review):
        return self.db.execute(
            text(
                """
                UPDATE REVIEWS 
                SET rating = :rating, text = :text
                WHERE user_id = :user_id AND supplement_id = :supplement_id
                """
            ),
            new_review,
        )

    def delete_review(self, user_id, supplement_id):
        return self.db.execute(
            text(
                """
                DELETE FROM REVIEWS
                WHERE user_id = :user_id AND supplement_id = :supplement_id
                """
            ),
            {"user_id": user_id, "supplement_id": supplement_id},
        )

    def get_rating(self, supplement_id):
        return self.db.execute(
            text(
                """
                SELECT avg_rating, rating_count
                FROM SUPPLEMENTS
                WHERE id=:supplement_id
                """
            ),
            {"supplement_id": supplement_id},
        ).fetchone()

    def increment_rating_count(self, supplement_id):
        return self.db.execute(
            text(
                """
                UPDATE SUPPLEMENTS
                SET rating_count = rating_count + 1
                WHERE id = :supplement_id
                """
            ),
            {"supplement_id": supplement_id},
        )

    def update_avg_rating(self, supplement_id, new_avg_rating):
        return self.db.execute(
            text(
                """
                UPDATE SUPPLEMENTS
                SET avg_rating = :new_avg_rating
                WHERE id = :supplement_id
                """
            ),
            {"new_avg_rating": new_avg_rating, "supplement_id": supplement_id},
        )

    def insert_img_url(self, review_id, img_url):
        return self.db.execute(
            text(
                """
                INSERT INTO REVIEW_IMGS (review_id, img_url)
                VALUES(:review_id, :img_url)
                """
            ),
            {"review_id": review_id, "img_url": img_url},
        )
