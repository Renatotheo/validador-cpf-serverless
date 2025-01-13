import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, BlobType
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Função para salvar capa de filme iniciada.')

    try:
        conteudo = req.get_body()
        nome_arquivo = req.params.get('nome')  # Ex: capa_filme_123.jpg
        if not nome_arquivo:
            return func.HttpResponse("Por favor, forneça o nome do arquivo da capa.", status_code=400)

        connect_str = os.environ["AzureWebJobsStorage"]
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "capas-filmes"  # Container para armazenar as capas
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=nome_arquivo, blob_type=BlobType.BlockBlob)
        blob_client.upload_blob(conteudo, overwrite=True)

        return func.HttpResponse(f"Capa '{nome_arquivo}' salva com sucesso.", status_code=200)

    except Exception as e:
        logging.error(f"Erro ao salvar capa: {e}")
        return func.HttpResponse(f"Erro ao salvar capa: {e}", status_code=500)