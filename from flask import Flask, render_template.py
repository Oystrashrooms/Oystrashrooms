from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_order():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    product = request.form['product']

    with open('orders.txt', 'a') as f:
        f.write(f'{name}, {phone}, {address}, {product}\n')

    return render_template('success.html', name=name)

@app.before_request
def log_visit():
    with open('clicks.log', 'a') as f:
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        path = request.path
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{time}, {ip}, {path}, {user_agent}\n')

@app.route('/track_click', methods=['POST'])
def track_custom_click():
    data = request.get_json()
    action = data.get('action')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('custom_clicks.csv', 'a') as f:
        f.write(f'{time},{ip},{action},{user_agent}\n')

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)