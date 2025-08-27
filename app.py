import base64
import os
import uuid
from types import NotImplementedType

import requests
from flask import Flask, jsonify, redirect, render_template, request, url_for
from typing_extensions import Dict

app = Flask(__name__)


def base64_encode(input):
    """Encode input to base64"""
    return base64.b64encode(input.encode()).decode()


class BasicClient:
    def __init__(self, url):
        self.url = url

    def is_ready(self) -> bool:
        """check server is ready"""
        ready_url = self.url.get("ready", None)
        if ready_url is None:
            return False
        response = requests.post(ready_url, json=dict())
        return response.status_code == 200

    def create_payload(self, input_dict: Dict) -> Dict:
        # TODO: support other shape
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

    def get_output(self, response: requests.Response) -> Dict:
        # TODO: return error message
        # TODO: support multi-output
        if response != 200:
            return dict()
        response_list = response.json().get("outputs", None)
        if response_list is None:
            return dict()
        result = dict()
        for i, resp in enumerate(response_list):
            name = resp.get("name", str(i))
            datatype = resp.get("datatype", None)
            data = resp.get("data", None)
            if datatype == "BYTES":
                result[name] = base64_encode(data.pop(0))
            else:
                result[name] = data.pop(0)
        return result

    def mock_infer(self) -> str | NotImplementedType:
        return NotImplemented

    def infer(self) -> str | NotImplementedType:
        return NotImplemented


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# --------------------- ESM3 Client --------------------------------------------
ESM3_HOST = os.getenv("ESM3_HOST", "http://localhost:8000")
ESM3_SERVER = f"{ESM3_HOST}/v2/models/ESM3"


class ESM3Client(BasicClient):
    def __init__(self, url):
        super().__init__(url)

    def mock_infer(self) -> str | NotImplementedType:
        resp = requests.post(
            "http://localhost:8000/mims/mock/esm3/prediction", json=dict()
        )
        result = resp.json()
        return render_template("index.html", outputs=result)

    def infer(self) -> str | NotImplementedType:
        return NotImplemented


esm3_client = ESM3Client(
    url={"ready": f"{ESM3_SERVER}/ready", "infer": f"{ESM3_SERVER}/infer"}
)
app.add_url_rule(
    rule="/run_esm3_prediction",
    endpoint="run_esm3_prediction",
    view_func=esm3_client.mock_infer,
    methods=["POST"],
)

# --------------------- MOFLOW Client --------------------------------------------
MOFLOW_HOST = os.getenv("MOFLOW_HOST", "http://localhost:8000")
MOFLOW_SERVER = f"{MOFLOW_HOST}/v2/models/ESM3"


class MoFlowClient(BasicClient):
    def __init__(self, url):
        super().__init__(url)

    def mock_infer(self):
        resp = requests.post(
            "http://localhost:8000/mims/mock/moflow/generation", json=dict()
        )
        result = resp.json()
        return render_template("index.html", outputs=result)

    def infer(self):
        return NotImplemented


moflow_client = MoFlowClient(
    url={"ready": f"{MOFLOW_SERVER}/ready", "infer": f"{MOFLOW_SERVER}/infer"}
)
app.add_url_rule(
    rule="/run_moflow_generation",
    endpoint="run_moflow_generation",
    view_func=moflow_client.mock_infer,
    methods=["POST"],
)


# --------------------- DIFFDOCK Client --------------------------------------------
DIFFDOCK_HOST = os.getenv("DIFFDOCK_HOST", "http://localhost:8000")
DIFFDOCK_SERVER = f"{DIFFDOCK_HOST}/v2/models/DIFFDOCK"


class DiffDockClient(BasicClient):
    def __init__(self, url):
        super().__init__(url)

    def mock_infer(self):
        resp = requests.post(
            "http://localhost:8000/mims/mock/diffdock/prediction", json=dict()
        )
        result = resp.json()
        return render_template("index.html", outputs=result)

    def infer(self):
        return NotImplemented


diffdock_client = DiffDockClient(
    url={"ready": f"{DIFFDOCK_SERVER}/ready", "infer": f"{DIFFDOCK_SERVER}/infer"}
)
app.add_url_rule(
    rule="/run_diffdock_prediction",
    endpoint="run_diffdock_prediction",
    view_func=diffdock_client.mock_infer,
    methods=["POST"],
)


if __name__ == "__main__":
    app.run(port=6006, debug=True)
