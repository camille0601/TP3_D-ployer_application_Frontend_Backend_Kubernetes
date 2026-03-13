from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Service Commandes Operationnel"

@app.route('/orders')
def get_orders():
    return jsonify([
        {"order_id": 101, "item": "Clavier"},
        {"order_id": 102, "item": "Souris"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)