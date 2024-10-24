from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,ShippingMethod
from flask_cors import CORS


shipping_method_bp = Blueprint('shipping_method', __name__, url_prefix='/shipping_method')
shipping_method_api = Api(shipping_method_bp)
CORS(shipping_method_bp)

shipping_method_parser = reqparse.RequestParser()
shipping_method_parser.add_argument('method_name', type=str, required=True, help='Method name is required')
shipping_method_parser.add_argument('cost', type=float, required=True, help='Cost is required')
shipping_method_parser.add_argument('estimated_delivery_time', type=str, required=False, help='Estimated delivery time is optional')

class ShippingMethodResource(Resource):
    def get(self, id):
        shipping_method = ShippingMethod.query.get(id)
        if shipping_method:
            return {
                'id': shipping_method.id,
                'method_name': shipping_method.method_name,
                'cost': shipping_method.cost,
                'estimated_delivery_time': shipping_method.estimated_delivery_time
            }, 200
        return {'message': 'Shipping method not found'}, 404

    def post(self):
        data = shipping_method_parser.parse_args()
        new_shipping_method = ShippingMethod(
            method_name=data['method_name'],
            cost=data['cost'],
            estimated_delivery_time=data['estimated_delivery_time']
        )
        db.session.add(new_shipping_method)
        db.session.commit()
        return {'message': 'Shipping method created successfully'}, 201

    def put(self, id):
        data = shipping_method_parser.parse_args()
        shipping_method = ShippingMethod.query.get(id)
        if shipping_method:
            shipping_method.method_name = data['method_name']
            shipping_method.cost = data['cost']
            shipping_method.estimated_delivery_time = data['estimated_delivery_time']
            db.session.commit()
            return {'message': 'Shipping method updated successfully'}, 200
        return {'message': 'Shipping method not found'}, 404

    def delete(self, id):
        shipping_method = ShippingMethod.query.get(id)
        if shipping_method:
            db.session.delete(shipping_method)
            db.session.commit()
            return {'message': 'Shipping method deleted successfully'}, 200
        return {'message': 'Shipping method not found'}, 404

shipping_method_api.add_resource(ShippingMethodResource, '/<int:id>')
