from flask import Blueprint, jsonify, request
from functools import wraps
from flask_restful import Api, Resource, reqparse
from models import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager, create_refresh_token, jwt_required, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message
from flask_cors import CORS

serializer = URLSafeTimedSerializer('We are winners')

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')
auth_api = Api(auth_bp)
bcrypt = Bcrypt()
jwt = JWTManager()
CORS(auth_bp)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

register_args = reqparse.RequestParser()
register_args.add_argument('full_name', type=str, required=True, help='Full name is required')
register_args.add_argument('email', type=str, required=True, help='Email is required')
register_args.add_argument('password', type=str, required=True, help='Password is required')
register_args.add_argument('password2', type=str, required=True, help='Please enter your password again')

login_args = reqparse.RequestParser()
login_args.add_argument('email', required=True, help='Email is required')
login_args.add_argument('password', required=True, help='Password is required')

class ResetPasswordRequest(Resource):
    def __init__(self, mail):
        self.mail = mail
    
    def post(self):
        data = request.get_json()
        email = data.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(email, salt='reset-password')
            user.reset_token = token
            # Uncomment if you want to set expiry
            # user.token_expiry = datetime.utcnow() + timedelta(hours=1)
            reset_url = f"http://localhost:5173/reset-password?token={token}"
            msg = Message("Password Reset Request",
                          sender="shinrafai@gmail.com",
                          recipients=[email])
            msg.body = f"Use this link to reset your password: {reset_url}"
            self.mail.send(msg)

        return jsonify({'message': 'If the email exists, a reset link has been sent.'})
    
class ResetPassword(Resource):
    def post(self):
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')
        
        try:
            email = serializer.loads(token, salt='reset-password', max_age=3600)
        except SignatureExpired:
            return jsonify({'message': 'The reset link is invalid or expired.'}), 400

        user = User.query.filter_by(email=email).first()
        if user:
            user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            db.session.commit()
            return jsonify({'message': 'Password has been reset.'})
        return jsonify({'message': 'User not found.'}), 404

class Register(Resource):
    def __init__(self, mail):
        self.mail = mail

    def post(self):
        data = register_args.parse_args()
        if data.get('password') != data.get('password2'):
            return {"message": "Passwords do not match"}, 400
        
        hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        new_user = User(full_name=data.get('full_name'), email=data.get('email'), password=hashed_password, confirmed=False)
        db.session.add(new_user)
        db.session.commit()
        
        token = serializer.dumps(data.get('email'), salt='email-confirm')
        confirm_url = f"http://localhost:5173/confirm-email?token={token}"
        msg = Message("Email Confirmation", sender="shinrafai@gmail.com", recipients=[data.get('email')])
        msg.body = f"Please confirm your email by clicking on the following link: {confirm_url}"
        self.mail.send(msg)
        
        return {"message": "User registration successful. A confirmation email has been sent."}, 201

class ConfirmEmail(Resource):
    def get(self):
        token = request.args.get('token')
        if not token:
            return {"message": "No confirmation token provided."}, 400
        
        try:
            email = serializer.loads(token, salt='email-confirm', max_age=3600)
        except SignatureExpired:
            return {"message": "The confirmation link has expired."}, 400
        except BadSignature:
            return {"message": "Invalid confirmation token."}, 400
        
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            return {"message": "Account already confirmed."}, 200
        
        user.confirmed = True
        db.session.commit()
        return {"message": "Your email has been confirmed. Thank you!"}, 200

class Login(Resource):
    def post(self):
        data = login_args.parse_args()
        user = User.query.filter_by(email=data.get('email')).first()

        if not user:
            return {"message": "User does not exist"}, 404
        if not bcrypt.check_password_hash(user.password, data.get('password')):
            return {"message": "Password does not match"}, 401

        token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {"token": token, "refresh_token": refresh_token}

    @jwt_required(refresh=True)
    def get(self):
        token = create_access_token(identity=current_user.id)
        return {"token": token}

class Logout(Resource):
    def delete(self):
        # Consider removing session management if JWT is used
        return {'message': 'You have successfully logged out'}, 200
    
def allow(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user
            user_role = user.role_id
            
            if user_role in allowed_roles:
                return fn(*args, **kwargs)
            
            return {"msg": "Access Denied"}, 403
        
        return wrapper
    return decorator


# Register resources
def create_resources(mail):
    auth_api.add_resource(Register, '/register', resource_class_kwargs={'mail': mail})
    auth_api.add_resource(Login, '/login')
    auth_api.add_resource(Logout, '/logout')
    auth_api.add_resource(ResetPasswordRequest, '/reset-password-request', resource_class_kwargs={'mail': mail})
    auth_api.add_resource(ResetPassword, '/reset-password')
    auth_api.add_resource(ConfirmEmail, '/confirm-email')
