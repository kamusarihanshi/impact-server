from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,OrderStatus
from flask_cors import CORS

order_status_bp = Blueprint('order_status', __name__, url_prefix='/order_status')
order_status_api = Api(order_status_bp)
CORS(order_status_bp)

order_status_parser = reqparse.RequestParser()
order_status_parser.add_argument('status_name', type=str, required=True, help='Status name is required')

class OrderStatusResource(Resource):
    def get(self, id):
        order_status = OrderStatus.query.get(id)
        if order_status:
            return {'id': order_status.id, 'status_name': order_status.status_name}, 200
        return {'message': 'Order status not found'}, 404

    def post(self):
        data = order_status_parser.parse_args()
        new_order_status = OrderStatus(status_name=data['status_name'])
        db.session.add(new_order_status)
        db.session.commit()
        return {'message': 'Order status created successfully'}, 201

    def put(self, id):
        data = order_status_parser.parse_args()
        order_status = OrderStatus.query.get(id)
        if order_status:
            order_status.status_name = data['status_name']
            db.session.commit()
            return {'message': 'Order status updated successfully'}, 200
        return {'message': 'Order status not found'}, 404
    
    def delete(self, id):
        order_status = OrderStatus.query.get(id)
        if order_status:
            db.session.delete(order_status)
            db.session.commit()
            return {'message': 'Order status deleted successfully'}, 200
        return {'message': 'Order status not found'}, 404

   
