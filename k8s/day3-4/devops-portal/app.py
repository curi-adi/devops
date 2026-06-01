from flask import Flask, render_template, jsonify
import os
import socket
import psycopg2

app = Flask(__name__)

DB_LINK = os.environ.get("DB_LINK", "")

def db_status():
    if not DB_LINK:
        return False, "DB_LINK not set"
    try:
        conn = psycopg2.connect(DB_LINK, connect_timeout=3)
        conn.close()
        return True, "connected"
    except Exception as e:
        return False, str(e)

@app.route("/health")
def health():
    ok, msg = db_status()
    status = "ok" if ok else "degraded"
    return jsonify({"status": status, "db": msg}), 200

@app.route("/")
def index():
    ok, msg = db_status()
    return render_template(
        "index.html",
        hostname=socket.gethostname(),
        pod_ip=socket.gethostbyname(socket.gethostname()),
        db_ok=ok,
        db_msg=msg,
        admin_user=os.environ.get("ADMIN_PASSWORD", "not set"),
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
