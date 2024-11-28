import json
import logging
from datetime import datetime
from services.s3_service import load_photo_from_query
from services.rekognition_service import detect_faces_and_emotions

# Configura o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler_v1(event, context):
    # Processa o corpo da requisição
    body = json.loads(event['body'])
    bucket = body.get('bucket')
    image_name = body.get('imageName')

    if not bucket or not image_name:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Parâmetros 'bucket' e 'imageName' são necessários."})
        }

    # Detecta as emoções usando o Rekognition
    try:
        faces = detect_faces_and_emotions(bucket, image_name)
        logger.info(f"Faces detectadas: {faces}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "url_to_image": f"https://{bucket}.s3.amazonaws.com/{image_name}",
                "created_image": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "faces": faces
            })
        }
    except Exception as e:
        logger.error(f"Erro ao processar a imagem no Rekognition: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Erro ao processar a imagem."})
        }