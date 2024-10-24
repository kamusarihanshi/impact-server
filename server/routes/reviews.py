from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,Review
from flask_cors import CORS
from datetime import datetime


review_bp=Blueprint('Review',__name__,url_prefix='/Review')
review_api=Api(review_bp)
CORS(review_bp)



review_parser = reqparse.RequestParser()
review_parser.add_argument('user_id', type=int, required=True, help='User ID is required')
review_parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
review_parser.add_argument('rating', type=int, required=True, help='Rating is required')
review_parser.add_argument('comment', type=str, required=True, help='Comment is required')

class ReviewResource(Resource):
    def get(self, id):
        review = Review.query.get(id)
        if review:
            return {
                'id': review.id,
                'user_id': review.user_id,
                'product_id': review.product_id,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at,
                'updated_at': review.updated_at
            }, 200
        return {'message': 'Review not found'}, 404

    def post(self):
        data = review_parser.parse_args()
        new_review = Review(
            user_id=data['user_id'],
            product_id=data['product_id'],
            rating=data['rating'],
            comment=data['comment']
        )
        db.session.add(new_review)
        db.session.commit()
        return {'message': 'Review created successfully'}, 201

    def put(self, id):
        data = review_parser.parse_args()
        review = Review.query.get(id)
        if review:
            review.rating = data['rating']
            review.comment = data['comment']
            db.session.commit()
            return {'message': 'Review updated successfully'}, 200
        return {'message': 'Review not found'}, 404

    def delete(self, id):
        review = Review.query.get(id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return {'message': 'Review deleted successfully'}, 200
        return {'message': 'Review not found'}, 404

review_api.add_resource(ReviewResource, '/<int:id>')
