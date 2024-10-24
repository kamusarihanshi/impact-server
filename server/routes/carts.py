from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,Cart,CartItem
from flask_cors import CORS



cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
cart_api = Api(cart_bp)
CORS(cart_bp)

class CartResource(Resource):
    def get(self, user_id):
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            return {'message': 'Cart not found'}, 404
        return {
            'id': cart.id,
            'user_id': cart.user_id,
            'created_at': cart.created_at,
            'updated_at': cart.updated_at,
            'cart_items': [{'id': item.id, 'product_id': item.product_id, 'quantity': item.quantity} for item in cart.cart_items]
        }, 200

    def post(self):
        data = reqparse.RequestParser().add_argument('user_id', type=int, required=True).parse_args()
        new_cart = Cart(user_id=data['user_id'])
        db.session.add(new_cart)
        db.session.commit()
        return {'message': 'Cart created successfully'}, 201

cart_api.add_resource(CartResource, '/<int:user_id>')


class CartItemResource(Resource):
    def post(self, cart_id):
        data = reqparse.RequestParser().add_argument('product_id', type=int, required=True).add_argument('quantity', type=int, required=True).parse_args()
        new_cart_item = CartItem(cart_id=cart_id, product_id=data['product_id'], quantity=data['quantity'])
        db.session.add(new_cart_item)
        db.session.commit()
        return {'message': 'Cart item added successfully'}, 201

    def delete(self, cart_id, item_id):
        cart_item = CartItem.query.filter_by(cart_id=cart_id, id=item_id).first()
        if not cart_item:
            return {'message': 'Cart item not found'}, 404
        db.session.delete(cart_item)
        db.session.commit()
        return {'message': 'Cart item deleted successfully'}, 200

cart_api.add_resource(CartItemResource, '/<int:cart_id>/item/<int:item_id>')
