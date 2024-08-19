from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.auth import auth_bp,jwt
from routes.reviews import reviews_bp
from routes.orders import order_bp
from routes.payments import payment_bp
from routes.categories import category_bp
from routes.products import product_bp
from models import db

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='12345'

db.init_app(app)
migrate = Migrate(app=app, db=db)
app.register_blueprint(auth_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(order_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(category_bp)
app.register_blueprint(product_bp)
jwt.init_app(app)



@app.route('/', methods=['GET'])
def movies():
    response_dict = {
        "text": "Movies will go here"
    }

    return make_response(jsonify(response_dict), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5555)