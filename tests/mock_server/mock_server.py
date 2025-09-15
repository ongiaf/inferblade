import argparse
import time

# Simple HTTP mock server using Flask for local testing
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/v2/models/esm3/infer", methods=["POST"])
def esm3_infer():
    j = request.get_json() or {}
    app.logger.debug("Request: %s", j)
    with open("./tests/data/1a46_protein_processed.pdb", "r") as f:
        pdb = f.read().strip()
    time.sleep(3)
    return jsonify({"output": [{"name": "pdb", "datatype": "BYTES", "data": [pdb]}]})


@app.route("/v2/models/moflow/infer", methods=["POST"])
def moflow_infer():
    j = request.get_json() or {}
    app.logger.debug("Request: %s", j)
    with open("./tests/data/1a46_ligand.sdf", "r") as f:
        sdf = f.read().strip()
    time.sleep(3)
    return jsonify({"output": [{"name": "sdf", "datatype": "BYTES", "data": [sdf]}]})


@app.route("/v2/models/diffdock/infer", methods=["POST"])
def diffdock_infer():
    j = request.get_json() or {}
    app.logger.debug("Request: %s", j)
    with open("./tests/data/1a46_ligand.sdf", "r") as f:
        sdf = f.read().strip()
    time.sleep(3)
    return jsonify({"output": [{"name": "sdf", "datatype": "BYTES", "data": [sdf]}]})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    app.run(port=args.port, debug=True)
