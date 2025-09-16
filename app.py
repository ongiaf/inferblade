import base64
import os
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

import requests
from flask import Blueprint, Flask, jsonify, render_template, request

app = Flask(__name__)


@dataclass
class ModelInformation:
    name: str
    key: str
    description: list
    tags: list


def create_payload(input_dict: Dict) -> Dict:
    payload = dict()
    payload["id"] = str(uuid.uuid4())
    payload["input"] = [
        {
            "name": key,
            "shape": [1, 1],
            "datatype": value["type"],
            "parameters": dict(),
            "data": [value["value"]],
        }
        for key, value in input_dict.items()
    ]
    return payload


def get_output(response: requests.Response) -> Dict:
    if response.status_code != 200:
        return {"error": "Response code is not 200."}
    response_json = response.json()
    if "error" in response_json:
        return response_json
    try:
        response_list = response_json["output"]
        result = dict()
        for i, resp in enumerate(response_list):
            name = resp.get("name", str(i))
            datatype = resp.get("datatype", None)
            data = resp.get("data", None)
            if datatype == "BYTES":
                result[name] = base64.b64encode(data.pop(0).encode()).decode()
            else:
                result[name] = data.pop(0)
        return result
    except Exception as exception:
        return {"error": exception}


DIFFDOCK_SERVER_HOST = os.getenv("DIFFDOCK_SERVER_HOST", "http://localhost:8000")
DIFFDOCK_SERVER = f"{DIFFDOCK_SERVER_HOST}/v2/models/diffdock"


class DiffDockClient:
    def __init__(self, url):
        self.url = url
        self.model = ModelInformation(
            name="DiffDock",
            key="diffdock",
            description=[
                "Predicts the 3D structure of how a molecule interacts with a protein."
            ],
            tags=["Biology", "Drug Discovery", "Docking"],
        )

    def index(self):
        return render_template("models/diffdock.html", model=self.model)

    def infer(self):
        try:
            inputs = {
                "diffdock_pdb": request.files["diffdock_pdb"].read().decode(),
                "diffdock_sdf": request.files["diffdock_sdf"].read().decode(),
            }
            payload_inputs = {
                "pdb": {"type": "BYTES", "value": inputs["diffdock_pdb"]},
                "sdf": {"type": "BYTES", "value": inputs["diffdock_sdf"]},
            }
            payload = create_payload(payload_inputs)
            response = requests.post(self.url, json=payload, timeout=(3, 300))
            result = get_output(response)
            if "error" not in result:
                result["pdb"] = base64.b64encode(
                    inputs["diffdock_pdb"].encode()
                ).decode()
            return render_template(
                "models/diffdock.html", model=self.model, outputs=result
            )
        except Exception as exception:
            app.logger.exception("DiffDock processing failed: %s", exception)
            return render_template(
                "models/diffdock.html", model=self.model, outputs={"error": exception}
            )


models = {"diffdock": DiffDockClient(url=f"{DIFFDOCK_SERVER}/infer")}


@app.route("/", methods=["GET"])
def index():
    models_info = [model.model for model in models.values()]
    return render_template("index.html", models=models_info)


for key, model in models.items():
    app.add_url_rule(
        f"/models/{key}",
        endpoint=f"{key}_index",
        view_func=model.index,
        methods=["GET"],
    )
    app.add_url_rule(
        f"/models/{key}/result",
        endpoint=f"{key}_result",
        view_func=model.infer,
        methods=["POST"],
    )


if __name__ == "__main__":
    app.run(port=6006, debug=True)
