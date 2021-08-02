import os

from datetime import date
from flask import current_app


class ReviewsService:
    def __init__(self, reviews_dao):
        self.reviews_dao = reviews_dao

    def get_review_id(self, user_id, supplement_id):
        review_id = self.reviews_dao.get_review_id(user_id, supplement_id)
        return review_id

    def get_reviews(self, user_id, supplement_id, page):
        # 페이지네이션 필요
        if user_id is not None and supplement_id is not None:
            review = self.reviews_dao.get_review(user_id, supplement_id)

            if review is None:
                return None

            review = review._asdict()
            review_imgs = self.reviews_dao.get_review_imgs(review["id"])

            new_review = {}
            new_review_imgs = []
            for review_img in review_imgs:
                new_review_imgs.append(review_img._asdict()["img_url"])

            new_review["imgUrls"] = new_review_imgs
            new_review["reviewId"] = review["id"]
            new_review["supplementId"] = review["supplement_id"]
            new_review["userId"] = review["user_id"]
            new_review["rating"] = review["rating"]
            new_review["text"] = review["text"]
            new_review["registrationDay"] = review["registration_day"]
            return new_review

        elif user_id is not None:
            reviews = self.reviews_dao.get_reviews_by_user_id(user_id, page)
        elif supplement_id is not None:
            reviews = self.reviews_dao.get_reviews_by_supplement_id(supplement_id, page)

        new_reviews = []
        for review in reviews:
            new_review = {}
            new_review["supplementId"] = review[0]
            new_review["supplementName"] = review[1]
            new_review["companyName"] = review[2]
            new_review["rating"] = review[3]
            new_reviews.append(new_review)
        return new_reviews

    def create_review(self, new_review):
        new_review["registration_day"] = date.today().strftime("%Y-%m-%d")
        review_id = self.reviews_dao.insert_review(new_review)
        supplement_id = new_review["supplement_id"]
        avg_rating, rating_count = self.reviews_dao.get_rating(supplement_id)
        new_avg_rating = ((avg_rating * rating_count) + int(new_review["rating"])) / (
            rating_count + 1
        )
        self.reviews_dao.increment_rating_count(supplement_id)
        self.reviews_dao.update_avg_rating(supplement_id, new_avg_rating)
        return review_id

    def upload_review_imgs(self, review_id, review_imgs):
        for img in review_imgs:
            img_path = os.path.join(current_app.config["MEDIA_URL"], img.filename)
            img.save(img_path)
            self.reviews_dao.insert_img_url(review_id, img_path)
        return None

    def update_review(self, new_review):
        self.reviews_dao.update_review(new_review)
        supplement_id = new_review["supplement_id"]
        avg_rating, rating_count = self.reviews_dao.get_rating(supplement_id)
        new_avg_rating = ((avg_rating * rating_count) + int(new_review["rating"])) / (
            rating_count + 1
        )
        self.reviews_dao.increment_rating_count(supplement_id)
        self.reviews_dao.update_avg_rating(supplement_id, new_avg_rating)
        return None

    def delete_review(self, user_id, supplement_id):
        review = self.get_review_id(user_id, supplement_id)
        review_id = review[0]
        imgs = self.reviews_dao.get_review_imgs(review_id)
        self.reviews_dao.delete_review(user_id, supplement_id)
        return None
