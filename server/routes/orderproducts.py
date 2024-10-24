from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,OrderProduct
from flask_cors import CORS




order_product_bp = Blueprint('order_product', __name__, url_prefix='/order_product')
order_product_api = Api(order_product_bp)
CORS(order_product_bp)

order_product_parser = reqparse.RequestParser()
order_product_parser.add_argument('order_id', type=int, required=True, help='Order ID is required')
order_product_parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
order_product_parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
order_product_parser.add_argument('price', type=float, required=True, help='Price is required')

class OrderProductResource(Resource):
    def get(self, order_id, product_id):
        order_product = OrderProduct.query.filter_by(order_id=order_id, product_id=product_id).first()
        if order_product:
            return {
                'order_id': order_product.order_id,
                'product_id': order_product.product_id,
                'quantity': order_product.quantity,
                'price': order_product.price
            }, 200
        return {'message': 'Order product not found'}, 404

    def post(self):
        data = order_product_parser.parse_args()
        new_order_product = OrderProduct(
            order_id=data['order_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            price=data['price']
        )
        db.session.add(new_order_product)
        db.session.commit()
        return {'message': 'Order product created successfully'}, 201

    def put(self, order_id, product_id):
        data = order_product_parser.parse_args()
        order_product = OrderProduct.query.filter_by(order_id=order_id, product_id=product_id).first()
        if order_product:
            order_product.quantity = data['quantity']
            order_product.price = data['price']
            db.session.commit()
            return {'message': 'Order product updated successfully'}, 200
        return {'message': 'Order product not found'}, 404

    def delete(self, order_id, product_id):
        order_product = OrderProduct.query.filter_by(order_id=order_id, product_id=product_id).first()
        if order_product:
            db.session.delete(order_product)
            db.session.commit()
            return {'message': 'Order product deleted successfully'}, 200
        return {'message': 'Order product not found'}, 404

order_product_api.add_resource(OrderProductResource, '/<int:order_id>/<int:product_id>')
