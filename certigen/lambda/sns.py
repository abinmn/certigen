import boto3
import json

class AwsSNS:
    
    def __init__(self):
        self.client = boto3.client(
            'sns',
            # aws_access_key_id=self.ACCESS_KEY_ID,
            # aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            # region_name=self.region
            )
    
    def publish_topic(self, arn, body):
        
        response = self.client.publish(
            TopicArn=arn,
            Message=json.dumps(body)
        )
        return response

    def send_email(self, email_template_id, recipients):
        arn = 'arn:aws:sns:ap-south-1:131829552397:send_email'
        body = {
            'email_template_id': email_template_id,
            'recipients': recipients
        }
        self.publish_topic(arn, body)

    def bulk_email_csv(self, csv_key, template_id):
        arn = 'arn:aws:sns:ap-south-1:131829552397:csv_email'
        body = {
            'csv_key': csv_key,
            'email_template_id': template_id
        }
        self.publish_topic(arn, body)