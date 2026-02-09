#!/usr/bin/env python3
from flask import Flask, request, jsonify
from datetime import datetime
import random
import sys

app = Flask(__name__)

# Configure logging to stdout (Docker logs)
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def log_request(status_code, response_size):
    """Generate Apache-style access log"""
    timestamp = datetime.now().strftime('%d/%b/%Y:%H:%M:%S +0000')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    method = request.method
    path = request.path
    user_agent = request.headers.get('User-Agent', '-')
    
    log_line = f'{ip} - - [{timestamp}] "{method} {path} HTTP/1.1" {status_code} {response_size} "-" "{user_agent}"'
    
    logging.info(log_line)

@app.route('/')
def home():
    response_size = random.randint(500, 2000)
    log_request(200, response_size)
    return jsonify({
        "message": "Welcome to Flask App",
        "status": "success"
    })

@app.route('/api/users')
def users():
    response_size = random.randint(1000, 5000)
    log_request(200, response_size)
    return jsonify({
        "users": ["user1", "user2", "user3"],
        "count": 3
    })

@app.route('/api/products')
def products():
    response_size = random.randint(2000, 10000)
    log_request(200, response_size)
    return jsonify({
        "products": ["product1", "product2"],
        "count": 2
    })

@app.route('/api/orders')
def orders():
    response_size = random.randint(1500, 8000)
    log_request(200, response_size)
    return jsonify({
        "orders": ["order1", "order2"],
        "count": 2
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Simulate some login failures
    if random.random() < 0.3:  # 30% failure rate
        response_size = random.randint(300, 800)
        log_request(401, response_size)
        return jsonify({"error": "Unauthorized"}), 401
    
    response_size = random.randint(500, 1500)
    log_request(200, response_size)
    return jsonify({"message": "Login successful"})

@app.route('/logout')
def logout():
    response_size = random.randint(200, 500)
    log_request(200, response_size)
    return jsonify({"message": "Logged out"})

@app.route('/admin')
def admin():
    # Simulate forbidden access
    if random.random() < 0.5:  # 50% forbidden
        response_size = random.randint(300, 600)
        log_request(403, response_size)
        return jsonify({"error": "Forbidden"}), 403
    
    response_size = random.randint(1000, 3000)
    log_request(200, response_size)
    return jsonify({"message": "Admin panel"})

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    if not query:
        response_size = random.randint(200, 400)
        log_request(400, response_size)
        return jsonify({"error": "Missing query parameter"}), 400
    
    response_size = random.randint(1000, 5000)
    log_request(200, response_size)
    return jsonify({
        "query": query,
        "results": []
    })

@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    # Simulate server errors occasionally
    if random.random() < 0.1:  # 10% server error
        response_size = random.randint(500, 1000)
        log_request(500, response_size)
        return jsonify({"error": "Internal Server Error"}), 500
    
    response_size = random.randint(2000, 8000)
    log_request(200, response_size)
    return jsonify({"message": "Checkout successful"})

@app.route('/static/<path:filename>')
def static_files(filename):
    response_size = random.randint(5000, 50000)
    log_request(200, response_size)
    return jsonify({"file": filename})

@app.errorhandler(404)
def not_found(e):
    response_size = random.randint(300, 600)
    log_request(404, response_size)
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    response_size = random.randint(500, 1000)
    log_request(500, response_size)
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Starting Flask app on 0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)