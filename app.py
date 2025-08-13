from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Handle order submission
@app.route('/submit', methods=['POST'])
def submit_order():
    name = request.form.get('name', '')
    phone = request.form.get('phone', '')
    address = request.form.get('address', '')
    product = request.form.get('product', '')

    # Ensure orders file exists and append data
    with open('orders.txt', 'a', encoding='utf-8') as f:
        f.write(f"{name}, {phone}, {address}, {product}\n")

    return render_template('success.html', name=name)

# Log every visit to the site
@app.before_request
def log_visit():
    with open('clicks.log', 'a', encoding='utf-8') as f:
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        path = request.path
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{time}, {ip}, {path}, {user_agent}\n")

# Track custom click events from JavaScript
@app.route('/track_click', methods=['POST'])
def track_custom_click():
    data = request.get_json(force=True)
    action = data.get('action', '')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('custom_clicks.csv', 'a', encoding='utf-8') as f:
        f.write(f"{time},{ip},{action},{user_agent}\n")

    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Use PORT from environment if available (important for Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
