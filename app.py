from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)
DATA_FILE = "orders.json"

def load_orders():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_orders(orders):
    with open(DATA_FILE, "w") as file:
        json.dump(orders, file, indent=4)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/place_order", methods=["POST"])
def place_order():
    data = request.json
    customer_name = data.get("customer_name")
    event_details = data.get("event_details")
    food_items = data.get("food_items")
    quantity = data.get("quantity")
    status = "Pending"

    orders = load_orders()
    new_order = {
        "order_id": len(orders) + 1,
        "customer_name": customer_name,
        "event_details": event_details,
        "food_items": food_items,
        "quantity": quantity,
        "status": status
    }
    orders.append(new_order)
    save_orders(orders)

    return jsonify({"message": "Order placed successfully!", "order_id": new_order["order_id"]})

@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.json
    order_id = data.get("order_id")
    new_status = data.get("status")

    orders = load_orders()
    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = new_status
            save_orders(orders)
            return jsonify({"message": "Order status updated successfully!"})

    return jsonify({"error": "Order not found"}), 404

@app.route("/view_orders", methods=["GET"])
def view_orders():
    return jsonify(load_orders())

@app.route("/generate_invoice", methods=["GET"])
def generate_invoice():
    order_id = int(request.args.get("order_id"))
    orders = load_orders()
    
    for order in orders:
        if order["order_id"] == order_id:
            invoice = f"""
            Invoice for Order #{order_id}
            Customer: {order['customer_name']}
            Event: {order['event_details']}
            Items: {order['food_items']} (x{order['quantity']})
            Status: {order['status']}
            """
            return jsonify({"invoice": invoice})

    return jsonify({"error": "Order not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
