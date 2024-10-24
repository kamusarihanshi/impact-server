from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,ProductAttribute
from flask_cors import CORS




product_attribute_bp = Blueprint('product_attribute', __name__, url_prefix='/product_attribute')
product_attribute_api = Api(product_attribute_bp)
CORS(product_attribute_bp)

product_attribute_parser = reqparse.RequestParser()
product_attribute_parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
product_attribute_parser.add_argument('attribute_name', type=str, required=True, help='Attribute name is required')
product_attribute_parser.add_argument('attribute_value', type=str, required=True, help='Attribute value is required')

class ProductAttributeResource(Resource):
    def get(self, id):
        product_attribute = ProductAttribute.query.get(id)
        if product_attribute:
            return {
                'id': product_attribute.id,
                'product_id': product_attribute.product_id,
                'attribute_name': product_attribute.attribute_name,
                'attribute_value': product_attribute.attribute_value
            }, 200
        return {'message': 'Product attribute not found'}, 404

    def post(self):
        data = product_attribute_parser.parse_args()
        new_product_attribute = ProductAttribute(
            product_id=data['product_id'],
            attribute_name=data['attribute_name'],
            attribute_value=data['attribute_value']
        )
        db.session.add(new_product_attribute)
        db.session.commit()
        return {'message': 'Product attribute created successfully'}, 201

    def put(self, id):
        data = product_attribute_parser.parse_args()
        product_attribute = ProductAttribute.query.get(id)
        if product_attribute:
            product_attribute.product_id = data['product_id']
            product_attribute.attribute_name = data['attribute_name']
            product_attribute.attribute_value = data['attribute_value']
            db.session.commit()
            return {'message': 'Product attribute updated successfully'}, 200
        return {'message': 'Product attribute not found'}, 404

    def delete(self, id):
        product_attribute = ProductAttribute.query.get(id)
        if product_attribute:
            db.session.delete(product_attribute)
            db.session.commit()
            return {'message': 'Product attribute deleted successfully'}, 200
        return {'message': 'Product attribute not found'}, 404

product_attribute_api.add_resource(ProductAttributeResource, '/<int:id>')
