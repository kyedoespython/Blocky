from flask import Blueprint, jsonify

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/test')
def test():
    return jsonify({"message": "Flask is running!"})