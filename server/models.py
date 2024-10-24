from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', back_populates='users')
    password = db.Column(db.String(250), nullable=False)

    reset_token = db.Column(db.String, nullable=True)
    token_expiry = db.Column(db.DateTime, nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    reviews = db.relationship('Review', back_populates='user')
    orders = db.relationship('Order', back_populates='user')
    wishlist = db.relationship('Wishlist', back_populates='user')
    cart = db.relationship('Cart', back_populates='user', uselist=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    users = db.relationship('User', back_populates='role')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(250), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='products')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    order_products = db.relationship('OrderProduct', back_populates='product')
    wishlists = db.relationship('Wishlist', back_populates='product')
    reviews = db.relationship('Review', back_populates='product')
    attributes = db.relationship('ProductAttribute', back_populates='product')
    cart_items = db.relationship('CartItem', back_populates='product')

class ProductAttribute(db.Model):
    __tablename__ = 'product_attributes'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    attribute_name = db.Column(db.String(80), nullable=False)
    attribute_value = db.Column(db.String(255), nullable=False)
    product = db.relationship('Product', back_populates='attributes')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    products = db.relationship('Product', back_populates='category')

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', back_populates='cart')
    cart_items = db.relationship('CartItem', back_populates='cart')

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cart = db.relationship('Cart', back_populates='cart_items')
    product = db.relationship('Product', back_populates='cart_items')

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    user = db.relationship('User', back_populates='wishlist')
    product = db.relationship('Product', back_populates='wishlists')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('order_status.id'), nullable=False)
    payment_method = db.Column(db.String(80), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    user = db.relationship('User', back_populates='orders')
    order_products = db.relationship('OrderProduct', back_populates='order')
    payment = db.relationship('Payment', back_populates='order', uselist=False)
    shipping_info = db.relationship('OrderShipping', back_populates='order', uselist=False)
    status = db.relationship('OrderStatus', back_populates='orders')

class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    order = db.relationship('Order', back_populates='order_products')
    product = db.relationship('Product', back_populates='order_products')

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    product = db.relationship('Product', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)
    transaction_id = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    status = db.Column(db.String(80), nullable=False)
    order = db.relationship('Order', back_populates='payment')

class ShippingMethod(db.Model):
    __tablename__ = 'shipping_methods'
    id = db.Column(db.Integer, primary_key=True)
    method_name = db.Column(db.String(80), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    estimated_delivery_time = db.Column(db.String(80), nullable=True)
    orders = db.relationship('OrderShipping', back_populates='shipping_method')

class OrderShipping(db.Model):
    __tablename__ = 'order_shipping'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    shipping_method_id = db.Column(db.Integer, db.ForeignKey('shipping_methods.id'), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    shipping_method = db.relationship('ShippingMethod', back_populates='orders')
    order = db.relationship('Order', back_populates='shipping_info')

class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(80), nullable=False, unique=True)
    orders = db.relationship('Order', back_populates='status')
