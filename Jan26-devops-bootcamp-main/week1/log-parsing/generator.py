#!/usr/bin/env python3
import random
import time
import requests
from datetime import datetime

FLASK_URL = "http://flask-app:5000"

# Simulate different endpoints
ENDPOINTS = [
    "/",
    "/api/users",
    "/api/products",
    "/api/orders",
    "/login",
    "/logout",
    "/admin",
    "/static/image.jpg",
    "/api/search?q=test",
    "/checkout",
    "/nonexistent",  # Will generate 404
    "/api/search",   # Will generate 400 (missing param)
]

# Simulate different user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "curl/7.68.0",
    "python-requests/2.28.0",
    "Googlebot/2.1",
    "BadBot/1.0",
    "Scanner/1.0"
]

# Simulate different IPs
IPS = [
    "192.168.1.100",
    "192.168.1.101", 
    "192.168.1.102",
    "10.0.0.50",
    "10.0.0.51",
    "172.16.0.10",
    "172.16.0.11",
    "203.0.113.42",  # Suspicious IP - will make many requests
    "198.51.100.50", # Another suspicious IP
]

def generate_traffic():
    """Generate realistic traffic patterns"""
    print("Waiting for Flask app to start...")
    time.sleep(10)
    print("Starting traffic generation...")
    
    request_count = 0
    
    while True:
        try:
            # Choose endpoint with weighted probability
            weights = [20, 15, 15, 10, 8, 5, 5, 5, 5, 5, 3, 2]  # Higher weight = more frequent
            endpoint = random.choices(ENDPOINTS, weights=weights)[0]
            
            user_agent = random.choice(USER_AGENTS)
            
            # Suspicious IPs make more requests
            if random.random() < 0.2:  # 20% from suspicious IPs
                ip = random.choice(["203.0.113.42", "198.51.100.50"])
            else:
                ip = random.choice(IPS)
            
            headers = {
                'User-Agent': user_agent,
                'X-Forwarded-For': ip
            }
            
            # Make request
            method = 'POST' if endpoint in ['/login', '/checkout'] and random.random() < 0.3 else 'GET'
            
            try:
                if method == 'POST':
                    response = requests.post(f"{FLASK_URL}{endpoint}", headers=headers, timeout=5)
                else:
                    response = requests.get(f"{FLASK_URL}{endpoint}", headers=headers, timeout=5)
                
                request_count += 1
                if request_count % 100 == 0:
                    print(f"Generated {request_count} requests...")
                    
            except requests.exceptions.RequestException as e:
                pass
            
            # Variable delay between requests
            # Suspicious IPs make faster requests
            if ip in ["203.0.113.42", "198.51.100.50"]:
                time.sleep(random.uniform(0.1, 0.5))  # Faster requests
            else:
                time.sleep(random.uniform(0.5, 3))    # Normal requests
            
        except Exception as e:
            print(f"Error generating traffic: {e}")
            time.sleep(5)

if __name__ == "__main__":
    generate_traffic()