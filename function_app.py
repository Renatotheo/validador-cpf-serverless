import logging
import json
import azure.functions as func
import re

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11:
        return False
    if len(set(cpf)) == 1:
        return False
    for i in range(9, 11):
        soma = 0
        for j in range(0, i):
            soma += int(cpf[j]) * (i + 1 - j)
        resto = (soma * 10) % 11
        if resto == 10 or resto != int(cpf[i]):
            return False
    return True

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="validar_cpf")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cpf = None
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        cpf = req_body.get('cpf')

    if not cpf:
        cpf = req.params.get('cpf')

    if cpf:
        valido = validar_cpf(cpf)
        return func.HttpResponse(
            json.dumps({"cpf": cpf, "valido": valido}),
            mimetype="application/json",
            status_code=200
        )
    else:
        return func.HttpResponse(
            "Por favor, forneça um CPF no corpo da requisição (JSON {'cpf': 'numero_cpf'}) ou via query string (?cpf=numero_cpf)",
            status_code=400
        )