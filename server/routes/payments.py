from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,Payment
from flask_cors import CORS
payment_bp=Blueprint('payment',__name__,url_prefix='/payment')
payment_api=Api(payment_bp)
CORS(payment_bp)

payment_parser=reqparse.RequestParser()
payment_parser.add_argument('order_id',type=int,required=True,help='Order ID is required')
payment_parser.add_argument('payment_date',type=str,required=True,help='Payment date is required')
payment_parser.add_argument('amount',type=float,required=True,help='Amount is required')
payment_parser.add_argument('payment_method',type=str,required=True,help='Payment method is required')
payment_parser.add_argument('status',type=str,required=True,help='Status is required')


class Payment(Resource):
    def post(self):
        data=payment_parser.parse_args()
        new_payment=Payment(order_id=data['order_id'],payment_date=data['payment_date'],amount=data['amount'],payment_method=data['payment_method'],status=data['status'])
        db.session.add(new_payment)
        db.session.commit()
        return {'message':'Payment added successfully'},201
    
    def get(self,id):
        payment=Payment.query.get(id)
        return{'order_id':payment.order_id, 'payment_date':payment.payment_date,'amount':payment.amount,'payment_method':payment.payment_method,'status':payment.status}
    
    def put(self,id):
        data=payment_parser.parse_args()
        payment=Payment.query.get(id)
        payment.order_id=data['order_id']
        payment.payment_date=data['payment_date']
        payment.amount=data['amount']
        payment.payment_method=data['payment_method']
        payment.status=data['status']
        db.session.commit()
        return {'message':'Payment updated successfully'}
    def delete(self,id):
        payment=Payment.query.get(id)
        db.session.delete(payment)
        db.session.commit()
        return {'message':'Payment deleted successfully'}
    


payment_api.add_resource(Payment,'/<int:id>')

class PaymentList(Resource):
    def get(self):
        payments=Payment.query.all()
        return [{'order_id':payment.order_id, 'payment_date':payment.payment_date,'amount':payment.amount,'payment_method':payment.payment_method,'status':payment.status} for payment in payments]
    
    def post(self):
        data=payment_parser.parse.args()
        new_payment=Payment(order_id=data['order_id'], amount=data['amount'], payment_date=data['payment_date'], payment_method=data['payment'], status=data['status'])
        db.session.add(new_payment)
        db.session.commit()
        return {'message':'Payment added successfully'},201
    
    def delete(self):
        payments=Payment.query.all()
        db.session.delete(payments)
        db.session.commit()
        return {'message':'All payments deleted successfully'}
    

payment_api.add_resource(PaymentList,'/list_payments')
