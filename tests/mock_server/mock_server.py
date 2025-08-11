import base64
import argparse

# Simple HTTP mock server using Flask for local testing
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/mims/mock/esm3/predict", methods=["POST"])
def esm3_predict():
    j = request.get_json() or {}
    seq = j.get("sequence", "")
    with open("./tests/data/1a46_protein_processed.pdb", "r") as f:
        pdb = f.read().strip()
    pdb_b64 = base64.b64encode(pdb.encode()).decode()
    return jsonify({"pdb": pdb_b64})


@app.route("/mims/mock/moflow/generation", methods=["POST"])
def moflow_predict():
    j = request.get_json() or {}
    seed = j.get("seed", "")
    with open("./tests/data/1a46_ligand.sdf", "r") as f:
        sdf = f.read().strip()
    sdf_b64 = base64.b64encode(sdf.encode()).decode()
    return jsonify({"sdf": sdf_b64})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    app.run(port=args.port, debug=True)
