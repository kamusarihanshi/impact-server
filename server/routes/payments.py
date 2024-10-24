from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,Payment
from flask_cors import CORS


payment_bp = Blueprint('payment', __name__, url_prefix='/payment')
payment_api = Api(payment_bp)
CORS(payment_bp)

payment_parser = reqparse.RequestParser()
payment_parser.add_argument('order_id', type=int, required=True, help='Order ID is required')
payment_parser.add_argument('amount', type=float, required=True, help='Amount is required')
payment_parser.add_argument('currency', type=str, required=True, help='Currency is required')
payment_parser.add_argument('payment_method', type=str, required=True, help='Payment method is required')
payment_parser.add_argument('payment_status', type=str, required=True, help='Payment status is required')
payment_parser.add_argument('transaction_id', type=str, required=True, help='Transaction ID is required')

class PaymentResource(Resource):
    def get(self, id):
        payment = Payment.query.get(id)
        if payment:
            return {
                'id': payment.id,
                'order_id': payment.order_id,
                'amount': payment.amount,
                'currency': payment.currency,
                'payment_method': payment.payment_method,
                'payment_status': payment.payment_status,
                'transaction_id': payment.transaction_id,
                'created_at': payment.created_at
            }, 200
        return {'message': 'Payment not found'}, 404

    def post(self):
        data = payment_parser.parse_args()
        new_payment = Payment(
            order_id=data['order_id'],
            amount=data['amount'],
            currency=data['currency'],
            payment_method=data['payment_method'],
            payment_status=data['payment_status'],
            transaction_id=data['transaction_id']
        )
        db.session.add(new_payment)
        db.session.commit()
        return {'message': 'Payment created successfully'}, 201

    def put(self, id):
        data = payment_parser.parse_args()
        payment = Payment.query.get(id)
        if payment:
            payment.amount = data['amount']
            payment.currency = data['currency']
            payment.payment_method = data['payment_method']
            payment.payment_status = data['payment_status']
            db.session.commit()
            return {'message': 'Payment updated successfully'}, 200
        return {'message': 'Payment not found'}, 404

    def delete(self, id):
        payment = Payment.query.get(id)
        if payment:
            db.session.delete(payment)
            db.session.commit()
            return {'message': 'Payment deleted successfully'}, 200
        return {'message': 'Payment not found'}, 404

payment_api.add_resource(PaymentResource, '/<int:id>')
