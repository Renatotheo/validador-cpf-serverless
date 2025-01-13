import logging
import azure.functions as func
import os
import json
import azure.cosmos.cosmos_client as cosmos_client

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Função para filtrar filmes iniciada.')

    try:
        parametro_filtro = req.params.get('parametro') # ex: genero, ano, titulo
        valor_filtro = req.params.get('valor') # ex: Ação, 2023, Vingadores
        if not parametro_filtro or not valor_filtro:
            return func.HttpResponse("Forneça os parâmetros 'parametro' e 'valor'.", status_code=400)

        endpoint = os.environ["CosmosDbConnectionString"].split(';')[0].split('=')[1]
        key = os.environ["CosmosDbConnectionString"].split(';')[1].split('=')[1]
        database_name = os.environ["CosmosDbConnectionString"].split(';')[2].split('=')[1]
        container_name = "filmes"

        client = cosmos_client.CosmosClient(url=endpoint, credential=key)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        query = f"SELECT * FROM c WHERE c.{parametro_filtro} = '{valor_filtro}'"
        itens = list(container.query_items(query=query, enable_cross_partition_query=True))

        return func.HttpResponse(json.dumps(itens), mimetype="application/json", status_code=200)

    except Exception as e:
        logging.error(f"Erro ao filtrar filmes: {e}")
        return func.HttpResponse(f"Erro ao filtrar filmes: {e}", status_code=500)