
from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import base64

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/run_esm3_predict', methods=['POST'])
def run_esm3_predict():
    payload = {}
    payload['sequence'] = request.form.get('sequence','')

    resp = requests.post('http://localhost:8000/mims/mock/esm3/predict', json=payload)
    data = resp.json()
    # pass outputs to template
    return render_template('index.html', outputs=data)


@app.route('/run_moflow_predict', methods=['POST'])
def run_moflow_predict():
    payload = {}
    payload['seed'] = request.form.get('seed',0)

    resp = requests.post('http://localhost:8000/mims/mock/moflow/predict', json=payload)
    data = resp.json()
    # pass outputs to template
    return render_template('index.html', outputs=data)


if __name__ == '__main__':
    app.run(port=6006, debug=True)
