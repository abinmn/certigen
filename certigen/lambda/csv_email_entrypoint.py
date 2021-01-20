import json
import boto3

from csv_utils import CSV_Utils
from sns import AwsSNS

sns = AwsSNS()

def get_file_name(path):
    i = path.rfind('/') + 1
    return path[i:]
    
def get_file_object(key):
    key = key.strip()
    filename = get_file_name(key)
    
    s3 = boto3.client('s3')
    bucket_name = 'storage.excelmec.tech'
    download_path = f'/tmp/{filename}'
    s3.download_file(bucket_name, key, download_path)
    return download_path
    
def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    email_template_id = message.get('email_template_id')
    csv_s3_path = message.get('csv_key')
    csv_file = get_file_object(csv_s3_path)
    
    csv_util = CSV_Utils(csv_file)
    recipients_chunk = csv_util.emails_as_chunks(11)
    for recipients in recipients_chunk:
        sns.send_email(email_template_id, recipients)
        print(recipients)
    return {
        'statusCode': 200,
    }
