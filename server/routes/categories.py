from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,Categories,Products
from flask_cors import CORS


category_bp=Blueprint('category',__name__,url_prefix='/category')
category_api=Api(category_bp)
CORS(category_bp)

category_parser=reqparse.RequestParser()
category_parser.add_argument('name',type=str,required=True,help='Name is required')
category_parser.add_argument('description',type=str,required=False,help='not required')

class Category(Resource):
    def get(self,id):
        category=Categories.query.get(id)
        return {'id':category.id, 'name':category.name, 'description':category.description}
    def post(self):
        data=category_parser.parse_args()
        new_category=Categories(name=data['name'], description=data['description'])
        db.session.add(new_category)
        db.session.commit()
        return {'message':'Category added successfully'},201
    def put(self,id):
        data=category_parser.parse_args()
        category=Categories.query.get(id)
        category.name=data['name']
        category.description=data['description']
        db.session.commit()
        return {'message':'Category updated successfully'},200
    def delete(self,id):
        category=Categories.query.get(id)
        db.session.delete(category)
        db.session.commit()
        return {'message':'Category deleted successfully'},200
    

category_api.add_resource(Category,'/<int:id>')


class CategoryList(Resource):
    def get(self):
        categories=Categories.query.all()
        return [{'id':category.id, 'name':category.name, 'description':category.description} for category in categories]
    
    def post(self):
        data=category_parser.parse_args()
        new_category=Categories(name=data['name'], description=data['description'])
        db.session.add(new_category)
        db.session.commit()
        return {'message':'Category added successfully'},201
    
    def delete(self):
        categories=Categories.query.all()
        db.session.delete(categories)
        db.session.commit()
        return {'message':'All categories deleted successfully'},200
    

category_api.add_resource(CategoryList,'/list_categories')

class ProductsByCategory(Resource):
    def get(self, category_id):
        category = Categories.query.get(category_id)
        if not category:
            return {'message': 'Category not found'}, 404
        
        products = Products.query.filter_by(category_id=category_id).all()
        return [{'id': product.id, 'name': product.name, 'price': product.price, 'stock': product.stock, 'image_url': product.image_url} for product in products], 200

        
        