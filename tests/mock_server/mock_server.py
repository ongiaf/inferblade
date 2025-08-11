import argparse
import base64

# Simple HTTP mock server using Flask for local testing
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/mims/mock/esm3/prediction", methods=["POST"])
def esm3_prediction():
    j = request.get_json() or {}
    with open("./tests/data/1a46_protein_processed.pdb", "r") as f:
        pdb = f.read().strip()
    pdb_b64 = base64.b64encode(pdb.encode()).decode()
    return jsonify({"pdb": pdb_b64})


@app.route("/mims/mock/moflow/generation", methods=["POST"])
def moflow_generation():
    j = request.get_json() or {}
    with open("./tests/data/1a46_ligand.sdf", "r") as f:
        sdf = f.read().strip()
    sdf_b64 = base64.b64encode(sdf.encode()).decode()
    return jsonify({"sdf": sdf_b64})


@app.route("/mims/mock/diffdock/prediction", methods=["POST"])
def diffdock_prediction():
    j = request.get_json() or {}
    with open("./tests/data/1a46_protein_processed.pdb", "r") as f:
        pdb = f.read().strip()
    pdb_b64 = base64.b64encode(pdb.encode()).decode()
    with open("./tests/data/1a46_ligand.sdf", "r") as f:
        sdf = f.read().strip()
    sdf_b64 = base64.b64encode(sdf.encode()).decode()
    return jsonify({"pdb": pdb_b64, "sdf": sdf_b64})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    app.run(port=args.port, debug=True)
