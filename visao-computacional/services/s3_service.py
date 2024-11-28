import os
import boto3
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def load_photo_from_query(bucket_name, file_name):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        return response['Body'].read()
    except Exception as e:
        logger.error(f"Erro ao carregar a imagem do S3: {str(e)}")
        return None

def get_file_data(bucket_name, file_name):
    try:
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        creation_date_str = s3.head_object(Bucket=bucket_name, Key=file_name)['LastModified'].isoformat()
        return image_url, creation_date_str
    except Exception as e:
        logger.error(f"Erro ao carregar dados do S3: {str(e)}")
        return None, None