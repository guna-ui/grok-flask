# routes.py
from flask import jsonify, request
from data import products, cart

def init_routes(app):
    @app.route('/')
    def home():
        return jsonify({"message": "Shopping Cart API"})

    @app.route('/products', methods=['GET'])
    def get_products():
        return jsonify({"products": products})

    @app.route('/cart', methods=['POST'])
    def add_to_cart():
        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)
        product = next((p for p in products if p["id"] == product_id), None)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        if product["stock"] < quantity:
            return jsonify({"error": "Insufficient stock"}), 400
        cart_item = {"product_id": product_id, "name": product["name"], "quantity": quantity, "price": product["price"]}
        cart.append(cart_item)
        return jsonify({"message": "Added to cart", "cart": cart}), 201
    
    @app.route('/products/<int:id>',methods=['GET'])
    def getProductbyId(id):
        product=next((p for p in products if p["id"]==id),None)
        if product:
            return jsonify(product)
        return jsonify({"error":"product not found"}),404