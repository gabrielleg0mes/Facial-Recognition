import boto3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

rekognition = boto3.client('rekognition')

def detect_faces_and_emotions(bucket_name, image_name):
    """Usa o Amazon Rekognition para detectar emoções em todas as faces de uma imagem."""
    try:
        response = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': image_name}},
            Attributes=['ALL']
        )

        if not response['FaceDetails']:
            return {
                "url_to_image": f"https://myphotos/{image_name}",
                "created_image": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "faces": [
                    {
                        "position": {
                            "Height": None,
                            "Left": None,
                            "Top": None,
                            "Width": None
                        },
                        "classified_emotion": None,
                        "classified_emotion_confidence": None
                    }
                ]
            }

        faces_data = []
        for face in response['FaceDetails']:
            emotions = face.get('Emotions', [])
            if emotions:
                primary_emotion = max(emotions, key=lambda e: e['Confidence'])
                face_info = {
                    "position": {
                        "Height": face['BoundingBox']['Height'],
                        "Left": face['BoundingBox']['Left'],
                        "Top": face['BoundingBox']['Top'],
                        "Width": face['BoundingBox']['Width']
                    },
                    "classified_emotion": primary_emotion['Type'],
                    "classified_emotion_confidence": primary_emotion['Confidence']
                }
                faces_data.append(face_info)

        return faces_data
    except Exception as e:
        logger.error(f"Erro ao detectar faces e emoções: {str(e)}")
        return []

def detect_pets(image_bytes):
    try:
        response = rekognition.detect_labels(Image={'Bytes': image_bytes})
        labels = []
        
        logger.info(f'Response Rekognition detect_labels: {response}')

        if not response.get('Labels'):
            return []

        for label in response['Labels']:
            if any(parent['Name'] == 'Pet' for parent in label['Parents']):
                labels.append({
                    "Name": label['Name'],
                    "Confidence": label['Confidence']
                })

        logger.info(f'Pets detectados: {labels}')
        return labels or []
    except Exception as e:
        logger.error(f"Erro ao detectar pets na imagem: {str(e)}")
        return []