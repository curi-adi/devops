from flask import Flask, render_template
import socket
import os

app = Flask(__name__)

@app.route('/')
def home():
    hostname = socket.gethostname()
    try:
        pod_ip = socket.gethostbyname(hostname)
    except Exception:
        pod_ip = "unknown"
    return render_template('index.html', hostname=hostname, pod_ip=pod_ip)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
