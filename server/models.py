from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)  
    reviews = db.relationship('Reviews', back_populates='user')
    orders = db.relationship('Orders', back_populates='user')

class Products(db.Model):
    __tablename__ = 'products_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(250), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories_table.id'), nullable=False)
    category = db.relationship('Categories', back_populates='products')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    order_products = db.relationship('OrderProduct', back_populates='product')
    reviews = db.relationship('Reviews', back_populates='product')

class Categories(db.Model):
    __tablename__ = 'categories_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)  
    description = db.Column(db.String(255), nullable=True)  
    products = db.relationship('Products', back_populates='category')

class Orders(db.Model):
    __tablename__ = 'orders_table'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(80), nullable=False)
    payment_method = db.Column(db.String(80), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)  
    user = db.relationship('User', back_populates='orders')
    order_products = db.relationship('OrderProduct', back_populates='order')
    payment = db.relationship('Payment', back_populates='order', uselist=False)

class OrderProduct(db.Model):
    __tablename__ = 'order_products_table'
    order_id = db.Column(db.Integer, db.ForeignKey('orders_table.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products_table.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    order = db.relationship('Orders', back_populates='order_products')
    product = db.relationship('Products', back_populates='order_products')

class Reviews(db.Model):
    __tablename__ = 'reviews_table'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products_table.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    product = db.relationship('Products', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

class Payment(db.Model):
    __tablename__ = 'payments_table'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders_table.id'), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)  
    order = db.relationship('Orders', back_populates='payment')
