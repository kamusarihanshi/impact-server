from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,Orders
from flask_cors import CORS
from datetime import datetime

order_bp=Blueprint('order',__name__,url_prefix='/order')
order_api=Api(order_bp)
CORS(order_bp)

order_parser=reqparse.RequestParser()
order_parser.add_argument('user_id',type=int,required=True,help='User ID is required')
order_parser.add_argument('product_id',type=int,required=True,help='Product ID is required')
order_parser.add_argument('order_date',type=datetime,required=True,help='date required')
order_parser.add_argument('total_amount',type=float,required=True,help='Total amount is required')
order_parser.add_argument('status',type=str,required=True,help='Status is required')
order_parser.add_argument('payment_method',type=str,required=True,help='Payment method is required')
order_parser.add_argument('shipping_address',type=str,required=True,help='Shipping address is required')



class OrderResource(Resource):
    def post(self):
        data=order_parser.parse_args()
        new_order=Orders(user_id=data['user_id'],product_id=data['product_id'],order_date=data['order_date'],total_amount=data['total_amount'],status=data['status'],payment_method=data['payment_method'],shipping_address=data['shipping_address'])
        db.session.add(new_order)
        db.session.commit()
        return {'message':'Order added successfully'},201
    
    def get(self,id):
        order=Orders.query.get(id)
        return{'user_id':order.user, 'product_id':order.product, 'order_id':order.order, 'order_date':order.order_date,'total_amount':order.total_amount,'status':order.status,'payment_method':order.payment_method,'shipping_method':order.shipping_address}
    
    def put(self,id):
        data=order_parser.parse_args()
        order=Orders.query.get(id)
        order.user_id=data['user_id']
        order.product_id=data['product_id']
        order.order_date=data['order_date']
        order.total_amount=data['total_amount']
        order.status=data['status']
        order.payment_method=data['payment_method']
        order.shipping_address=data['shipping_address']
        db.session.commit()
        return {'message':'Order updated successfully'}
    
    def delete(self,id):
        order=Orders.query.get(id)
        db.session.delete(order)
        db.session.commit()
        return {'message':'Order deleted successfully'}
    

order_api.add_resource(OrderResource,'/<int:id>')

class OrderListResource(Resource):
    def get(self):
        orders=Orders.query.all()
        return [{'user_id':order.user, 'product_id':order.product, 'order_id':order.order, 'order_date':order.order_date,'total_amount':order.total_amount,'status':order.status,'payment_method':order.payment_method,'shipping_address':order.shipping_address} for order in orders]
    
    def post(self):
        data=order_parser.parse_args()
        new_order=Orders(user_id=data['user_id'],product_id=data['product_id'],order_date=data['order_date'],total_amount=data['total_amount'],status=data['status'],payment_method=data['payment_method'],shipping_address=data['shipping_address'])
        db.session.add(new_order)
        db.session.commit()
        return {'message':'Order added successfully'},201
    
    def delete(self):
        orders=Orders.query.all()
        db.session.delete(orders)
        db.session.commit()
        return {'message':'All orders deleted successfully'}
    


order_api.add_resource(OrderListResource,'/list_orders')


    