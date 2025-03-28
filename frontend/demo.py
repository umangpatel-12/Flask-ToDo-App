import os
from flask import Flask, request, render_template, jsonify  # type: ignore
from datetime import datetime
import requests

BACKEND_URL = "http://localhost:9000"

app = Flask(__name__)

@app.route('/')
def index():
    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.today().strftime('%H:%M:%S')
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    try:
        if request.method == 'POST':
            form_data = dict(request.json)
        else:
            form_data = dict(request.args)

        response = requests.post(BACKEND_URL + "/submit", json=form_data)
        response.raise_for_status()  # Raise an error for HTTP errors

        return "Data submitted successfully in MongoDB"
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Unable to connect to the backend. Please ensure the backend is running.'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)