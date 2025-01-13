import logging
import json
import azure.functions as func
from flask import Flask, jsonify, request

bp = Flask(__name__)

@bp.route('/bem vindo', methods=['GET'])
def hello():
    return jsonify({"message": "simulando azure Functions!"})

@bp.route('/hello/<nome>', methods=['GET'])
def hello_nome(nome):
    return jsonify({"message": f"Olá, {nome}!"})

@bp.route('/data', methods=['POST'])
def receive_data():
    try:
        req_body = request.get_json()
    except ValueError:
        return jsonify({"error": "Corpo da requisição inválido (JSON esperado)"}), 400
    else:
        return jsonify(req_body), 200

def main(req: func.HttpRequest) -> func.HttpResponse:
    with bp.request_context(req.environ):
        return bp.full_dispatch_request()