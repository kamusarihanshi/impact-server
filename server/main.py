from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.auth import auth_bp,jwt
from routes.reviews import review_bp
from routes.shippingmethod import shipping_method_bp
from routes.wishlist import wishlist_bp
from routes.orders import order_bp
from routes.categories import category_bp
from routes.payments import payment_bp
from routes.admin import admin_bp

from routes.orderstatus import order_status_bp
from routes.ordershipping import order_shipping_bp
from routes.productattribute import product_attribute_bp
from routes.orderproducts import order_product_bp
from routes.products import product_bp
from routes.auth import auth_bp
from models import db
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)




app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='H12345'

db.init_app(app)
migrate = Migrate(app=app, db=db)



app.register_blueprint(auth_bp)
app.register_blueprint(order_bp)
app.register_blueprint(category_bp)
app.register_blueprint(product_bp)
app.register_blueprint(review_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(shipping_method_bp)
app.register_blueprint(product_attribute_bp)
app.register_blueprint(order_product_bp)
app.register_blueprint(order_shipping_bp)
app.register_blueprint(wishlist_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(order_status_bp)



jwt.init_app(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = ('shinrafai@gmail.com')
app.config['MAIL_PASSWORD'] = ('hanshi7')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
CORS(app)



@app.route('/', methods=['GET'])
def movies():
    response_dict = {
        "text": "Movies will go here"
    }

    return make_response(jsonify(response_dict), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=6055)