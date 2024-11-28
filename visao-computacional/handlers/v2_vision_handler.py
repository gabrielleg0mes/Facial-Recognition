import json
import logging
from services.s3_service import load_photo_from_query, get_file_data
from services.rekognition_service import detect_faces_and_emotions, detect_pets
from services.bedrock_service import generate_pet_tips

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler_v2(event, context):
    logger.info(f'Recebido evento: {event}')  # Log do evento recebido
    body = event.get('body')
    
    if not body:
        return {
            "statusCode": 400,
            "body": json.dumps({"Message": "Parâmetros 'bucket' e 'imageName' são necessários."})
        }
    
    try:
        body = json.loads(body)  # Tente carregar o corpo aqui
    except json.JSONDecodeError as e:
        logger.error(f'Erro ao decodificar o JSON: {str(e)}')
        return {
            "statusCode": 400,
            "body": json.dumps({"Message": "Corpo da solicitação não é um JSON válido."})
        }

    bucket = body.get('bucket')
    image_name = body.get('imageName')

    if not bucket or not image_name:
        return {
            "statusCode": 400,
            "body": json.dumps({"Message": "Parâmetros 'bucket' e 'imageName' são necessários."})
        }

    try:
        image = load_photo_from_query(bucket_name=bucket, file_name=image_name)
        if image is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"Message": "Imagem não encontrada no S3."})
            }
        
        image_url, date = get_file_data(bucket, image_name)
        if image_url is None or date is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"Message": "Dados da imagem não encontrados."})
            }
    except Exception as e:
        logger.error(f'Erro ao carregar imagem S3: {e}')
        return {
            "statusCode": 500,
            "body": json.dumps({"Message": "Erro ao carregar imagem S3"})
        }

    try:
        emotions = detect_faces_and_emotions(bucket, image_name)
        logger.info(f'Emoções detectadas: {emotions}')

        pets = detect_pets(image)
        logger.info(f'Pets detectados: {pets}')

        for pet in pets:
            pet_name = pet.get('Name')
            pet['Dicas'] = generate_pet_tips(pet_name) or "Nenhuma dica disponível."
    except Exception as e:
        logger.error(f'Erro ao processar imagem: {e}')
        return {
            "statusCode": 500,
            "body": json.dumps({"Message": "Erro ao processar imagem"})
        }

    response_body = {
        "url_to_image": image_url,
        "created_image": date,
        "pets": [
            {
                "labels": [
                    {"Confidence": pet['Confidence'], "Name": pet['Name']} for pet in pets if isinstance(pet, dict)
                ],
                "Dicas": pet.get('Dicas', "Nenhuma dica disponível.").replace('\n', ' ')
            }
            for pet in pets if isinstance(pet, dict)
        ],
        "faces": emotions or []
    }

    logger.info(f'Resposta gerada: {response_body}')
    return {
        "statusCode": 200,
        "body": json.dumps(response_body, ensure_ascii=False)
    }
