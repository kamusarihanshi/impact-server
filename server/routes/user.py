from flask_restful import Api, Resource, reqparse
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import User,db
from sqlalchemy.exc import SQLAlchemyError

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
user_api = Api(user_bp)

class GetUserById(Resource):
    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()

        if current_user_id != id:
            return {'message': 'Unauthorized to delete this account'}, 403

        try:
            user = User.query.get_or_404(id)
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred', 'error': str(e)}, 500
        
    @jwt_required()
    def get(self,id):
        current_user_id = get_jwt_identity()

        if current_user_id!= id:
            return {'message': 'Unauthorized to view this account'}, 403

        user = User.query.get_or_404(id)
        return {'full_name': user.full_name,'email': user.email} 
    

user_api.add_resource(GetUserById, '/<int:id>/delete')
