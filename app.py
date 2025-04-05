from flask import Flask,jsonify,request

app=Flask(__name__)

products=[
    {"id":1,"name":"tcs","price":3000,"stocks":5},
    {"id":2,"name":"infy","price":1500,"stocks":4},
    {"id":3,"name":"HCL","price":2000,"stocks":3},
    {"id":4,"name":"DR Reddy","price":1300,"stocks":15}
]

cart=[]

@app.route('/')
def home():
    return jsonify({"message":"Shopping Cart API"})

@app.route('/products',methods=['GET'])
def getproducts():
    return jsonify({"products":products})

@app.route('/products/<int:product_id>',methods=['GET'])
def getproduct(product_id):
    product=next((p for p in products if p["id"]==product_id),None)
    if product:
        return jsonify(product)
    return jsonify({"error":"Product not found"})

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    if product["stocks"] < quantity:
        return jsonify({"error": "Insufficient stock"}), 400

    # Check if product is already in cart
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            return jsonify({"message": "Updated cart", "cart": cart}), 200

    cart_item = {"product_id": product_id, "name": product["name"], "quantity": quantity, "price": product["price"]}
    cart.append(cart_item)
    return jsonify({"message": "Added to cart", "cart": cart}), 201

if __name__=="__main__":
    app.run(debug=True)