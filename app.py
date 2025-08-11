import base64

import requests
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/run_esm3_prediction", methods=["POST"])
def run_esm3_predict():
    payload = {}
    payload["sequence"] = request.form.get("esm3_sequence", "")

    resp = requests.post(
        "http://localhost:8000/mims/mock/esm3/prediction", json=payload
    )
    data = resp.json()
    # pass outputs to template
    return render_template("index.html", outputs=data)


@app.route("/run_moflow_generation", methods=["POST"])
def run_moflow_generation():
    payload = {}
    payload["seed"] = request.form.get("moflow_seed", 0)

    resp = requests.post(
        "http://localhost:8000/mims/mock/moflow/generation", json=payload
    )
    data = resp.json()
    # pass outputs to template
    return render_template("index.html", outputs=data)


@app.route("/run_diffdock_prediction", methods=["POST"])
def run_diffdock_prediction():
    payload = {}
    payload["pdb"] = request.form.get("diffdock_pdb", "")
    payload["sdf"] = request.form.get("diffdock_sdf", "")

    resp = requests.post(
        "http://localhost:8000/mims/mock/diffdock/prediction", json=payload
    )
    data = resp.json()
    # pass outputs to template
    return render_template("index.html", outputs=data)


if __name__ == "__main__":
    app.run(port=6006, debug=True)
