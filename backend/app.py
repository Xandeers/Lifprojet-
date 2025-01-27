from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

products = [
    {
        'id': 1,
        'name': 'Tomate',
        'category': 'vrac',
        'nutrients': {
            'calories': 10,
            'total_fat': 10,
            'sodium': 10,
            'total_sugars': 10
        }
    },
    {
        'id': 2,
        'name': 'Orange',
        'category': 'vrac',
        'nutrients': {
            'calories': 10,
            'total_fat': 10,
            'sodium': 10,
            'total_sugars': 10
        }
    }
]

# Products endpoint

@app.route("/api/products")
def get_products():
    return jsonify(products)

@app.route("/api/products", methods=['POST'])
def add_product():
    products.append(request.get_json())
    return '', 204

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)