from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,Wishlist
from flask_cors import CORS



wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')
wishlist_api = Api(wishlist_bp)
CORS(wishlist_bp)

class WishlistResource(Resource):
    def get(self, user_id):
        wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
        return [{'product_id': item.product_id} for item in wishlist_items], 200

    def post(self, user_id):
        data = reqparse.RequestParser().add_argument('product_id', type=int, required=True).parse_args()
        new_wishlist_item = Wishlist(user_id=user_id, product_id=data['product_id'])
        db.session.add(new_wishlist_item)
        db.session.commit()
        return {'message': 'Wishlist item added successfully'}, 201

    def delete(self, user_id, product_id):
        wishlist_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
        if not wishlist_item:
            return {'message': 'Wishlist item not found'}, 404
        db.session.delete(wishlist_item)
        db.session.commit()
        return {'message': 'Wishlist item deleted successfully'}, 200

wishlist_api.add_resource(WishlistResource, '/<int:user_id>')
