import json
import urllib.request
from ses import AmazonSes

SENDER = "Excel MEC <noreply@excelmec.tech>"
HEADER_TO_ADDRESS = "attendees@excelmec.tech"
CONFIGURATION_SET = "ConfigSet"


def lambda_handler(event, context):
    
    message = json.loads(event['Records'][0]['Sns']['Message'])
    email_template_id = message.get('email_template_id')
    recipients = message.get('recipients')

    r = urllib.request.urlopen(urllib.request.Request(
        url=f'https://excelmec-email.herokuapp.com/api/emails/{email_template_id}',
        headers={'Accept': 'application/json'},
        method='GET'),
    timeout=5)
    
    body = json.loads(r.read())
    subject = body.get('subject')
    body_text = body.get('body_plain_text')
    body_html = body.get('body_html_text')

    ses = AmazonSes(
            RECIPIENTS=recipients,
            SENDER=SENDER,
            SUBJECT=subject,
            BODY_TEXT=body_text,
            BODY_HTML=body_html,
            HEADER_TO_ADDRESS=HEADER_TO_ADDRESS,
            ATTACHMENT=None
        )
    ses.send_email()
    return {
        'statusCode': 200,
        'subject': subject,
        'recipients': recipients
    }
