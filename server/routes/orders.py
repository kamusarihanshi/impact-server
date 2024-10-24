from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from models import db, Order
from flask_cors import CORS
from datetime import datetime

order_bp = Blueprint('order', __name__, url_prefix='/order')
order_api = Api(order_bp)
CORS(order_bp)

order_parser = reqparse.RequestParser()
order_parser.add_argument('user_id', type=int, required=True, help='User ID is required')
order_parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
order_parser.add_argument('order_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=True, help='Date required in YYYY-MM-DD format')
order_parser.add_argument('total_amount', type=float, required=True, help='Total amount is required')
order_parser.add_argument('status', type=str, required=True, help='Status is required')
order_parser.add_argument('payment_method', type=str, required=True, help='Payment method is required')
order_parser.add_argument('shipping_address', type=str, required=True, help='Shipping address is required')


class OrderResource(Resource):
    def get(self, user_id):
        orders = Order.query.filter_by(user_id=user_id).all()
        return [{'id': order.id, 'total_amount': order.total_amount, 'status_id': order.status_id} for order in orders], 200

    def post(self):
        data = reqparse.RequestParser().add_argument('user_id', type=int, required=True).add_argument('total_amount', type=float, required=True).add_argument('payment_method', type=str, required=True).add_argument('shipping_address', type=str, required=True).parse_args()
        new_order = Order(user_id=data['user_id'], total_amount=data['total_amount'], payment_method=data['payment_method'], shipping_address=data['shipping_address'])
        db.session.add(new_order)
        db.session.commit()
        return {'message': 'Order created successfully'}, 201

    def delete(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return {'message': 'Order not found'}, 404
        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted successfully'}, 200

order_api.add_resource(OrderResource, '/<int:user_id>')
