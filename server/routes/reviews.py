from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,Reviews
from flask_cors import CORS
from datetime import datetime


reviews_bp=Blueprint('reviews',__name__,url_prefix='/reviews')
reviews_api=Api(reviews_bp)
CORS(reviews_bp)

review_parser=reqparse.RequestParser()
review_parser.add_argument('product_id',type=int,required=True,help='Product ID is required')
review_parser.add_argument('rating',type=int,required=True,help='Rating is required')
review_parser.add_argument('comment',type=str,required=True,help='Comment is required')
review_parser.add_argument('created_at',type=datetime,required=True,help='created_at is required')
review_parser.add_argument('updated_at',type=datetime,required=True, help='updated_at is required')

class Review(Resource):
    def get(self,id):
        review=Reviews.query.get_or_404(id)
        return {'product_id':review.product_id,'rating':review.rating,'comment':review.comment,'created_at':review.created_at,'updated_at':review.updated_at}
    
    def put(self,id):
        data=review_parser.parse_args()
        review=Reviews.query.get_or_404(id)
        review.product_id=data['product_id']
        review.rating=data['rating']
        review.comment=data['comment']
        review.created_at=data['created_at']
        review.updated_at=data['updated_at']
        db.session.commit()
        return {'message':'Review updated successfully'}
    
    def delete(self,id):
        review=Reviews.query.get_or_404(id)
        db.session.delete(review)
        db.session.commit()
        return {'message':'Review deleted successfully'}
    

reviews_api.add_resource(Review,'/<int:id>')

class ReviewList(Resource):
    def get(self):
        reviews=Reviews.query.all()
        return [{'product_id':review.product_id,'rating':review.rating,'comment':review.comment,'created_at':review.created_at,'updated_at':review.updated_at} for review in reviews]
    
    def post(self):
        data=review_parser.parse_args()
        new_review=Reviews(product_id=data['product_id'],rating=data['rating'],comment=data['comment'],created_at=data['created_at'],updated_at=data['updated_at'])
        db.session.add(new_review)
        db.session.commit()
        return {'message':'Review added successfully'},201
    
    def delete(self):
        reviews=Reviews.query.all()
        db.session.delete(reviews)
        db.session.commit()
        return {'message':'All reviews deleted successfully'}
    


reviews_api.add_resource(ReviewList,'/list_reviews')

