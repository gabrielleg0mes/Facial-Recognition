import json
import logging
import boto3
import time

bedrock_client = boto3.client('bedrock-runtime')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ImageError(Exception):
    "Exceção personalizada para erros retornados pelos modelos Amazon Titan Text."
    def __init__(self, message):
        self.message = message

def generate_pet_tips(pet_name):
    prompt = f"A partir da imagem do {pet_name}, gere dicas sobre os cuidados, temperamento, nível de energia e problemas de saúde comuns."
    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 3072,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 0.9
        }
    })

    try:
        # Logar o tempo de início
        start_time = time.time()
        
        # Enviar a mensagem para o modelo
        response = bedrock_client.invoke_model(
            modelId='amazon.titan-text-premier-v1:0',
            body=body,
            accept="application/json",
            contentType="application/json"
        )
        
        # Logar o tempo de término
        end_time = time.time()
        
        # Calcular o tempo total de execução
        elapsed_time = end_time - start_time
        logger.info(f"Tempo total de execução: {elapsed_time:.2f} segundos")
        
        # Processar a resposta
        response_body = json.loads(response.get("body").read().decode('utf-8'))
        
        if "error" in response_body:
            raise ImageError(f"Erro na geração de texto: {response_body['error']}")

        return response_body['results'][0]['outputText']
    except Exception as e:
        logger.error(f'Erro ao chamar Bedrock: {e}')
        return "Não foi possível gerar dicas no momento."

if __name__ == "__main__":
    tips = generate_pet_tips("Dog")
    print(tips)