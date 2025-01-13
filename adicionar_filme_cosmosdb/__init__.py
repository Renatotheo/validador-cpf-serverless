import logging
import azure.functions as func
import os
import json
import azure.cosmos.cosmos_client as cosmos_client

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Função para adicionar filme iniciada.')

    try:
        req_body = req.get_json()

        endpoint = os.environ["CosmosDbConnectionString"].split(';')[0].split('=')[1]
        key = os.environ["CosmosDbConnectionString"].split(';')[1].split('=')[1]
        database_name = os.environ["CosmosDbConnectionString"].split(';')[2].split('=')[1]
        container_name = "filmes" #nome do container

        client = cosmos_client.CosmosClient(url=endpoint, credential=key)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        
        container.create_item(body=req_body)

        return func.HttpResponse("Filme adicionado ao catálogo com sucesso.", status_code=200)

    except ValueError:
        return func.HttpResponse("Corpo da requisição inválido (JSON esperado).", status_code=400)
    except Exception as e:
        logging.error(f"Erro ao adicionar filme: {e}")
        return func.HttpResponse(f"Erro ao adicionar filme: {e}", status_code=500)