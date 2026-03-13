from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# On autorise le frontend à appeler cette API
CORS(app)

@app.route('/api/message')
def get_message():
    return jsonify({"message": "Hello from backend"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)