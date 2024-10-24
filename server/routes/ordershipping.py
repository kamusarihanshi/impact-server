from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,OrderShipping
from flask_cors import CORS


order_shipping_bp = Blueprint('order_shipping', __name__, url_prefix='/order_shipping')
order_shipping_api = Api(order_shipping_bp)
CORS(order_shipping_bp)

order_shipping_parser = reqparse.RequestParser()
order_shipping_parser.add_argument('order_id', type=int, required=True, help='Order ID is required')
order_shipping_parser.add_argument('shipping_method_id', type=int, required=True, help='Shipping method ID is required')
order_shipping_parser.add_argument('shipping_address', type=str, required=True, help='Shipping address is required')

class OrderShippingResource(Resource):
    def get(self, order_id):
        order_shipping = OrderShipping.query.get(order_id)
        if order_shipping:
            return {
                'order_id': order_shipping.order_id,
                'shipping_method_id': order_shipping.shipping_method_id,
                'shipping_address': order_shipping.shipping_address
            }, 200
        return {'message': 'Order shipping not found'}, 404

    def post(self):
        data = order_shipping_parser.parse_args()
        new_order_shipping = OrderShipping(
            order_id=data['order_id'],
            shipping_method_id=data['shipping_method_id'],
            shipping_address=data['shipping_address']
        )
        db.session.add(new_order_shipping)
        db.session.commit()
        return {'message': 'Order shipping created successfully'}, 201

    def put(self, order_id):
        data = order_shipping_parser.parse_args()
        order_shipping = OrderShipping.query.get(order_id)
        if order_shipping:
            order_shipping.shipping_method_id = data['shipping_method_id']
            order_shipping.shipping_address = data['shipping_address']
            db.session.commit()
            return {'message': 'Order shipping updated successfully'}, 200
        return {'message': 'Order shipping not found'}, 404

    def delete(self, order_id):
        order_shipping = OrderShipping.query.get(order_id)
        if order_shipping:
            db.session.delete(order_shipping)
            db.session.commit()
            return {'message': 'Order shipping deleted successfully'}, 200
        return {'message': 'Order shipping not found'}, 404

order_shipping_api.add_resource(OrderShippingResource, '/<int:order_id>')
