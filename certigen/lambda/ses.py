import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class AmazonSes():

    def __init__(self, RECIPIENTS, SUBJECT,
                 BODY_TEXT, BODY_HTML,
                 HEADER_TO_ADDRESS=None,
                 SENDER="Excel MEC <noreply@excelmec.tech>",
                 ATTACHMENT=None,
                 AWS_REGION="ap-south-1",
                 CONFIGURATION_SET="ConfigSet",
                 CHARSET="utf-8"):
        self.SENDER = SENDER
        self.RECIPIENTS = RECIPIENTS
        self.HEADER_TO_ADDRESS = HEADER_TO_ADDRESS
        self.AWS_REGION = AWS_REGION
        self.SUBJECT = SUBJECT
        self.ATTACHMENT = ATTACHMENT
        self.BODY_TEXT = BODY_TEXT
        self.BODY_HTML = BODY_HTML
        self.CHARSET = CHARSET
        self.CONFIGURATION_SET = CONFIGURATION_SET

        self.ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    def create_message(self):
        """Create and return message with headers, subject, body
           and/or attachments."""

        message = MIMEMultipart('mixed')

        # Set message header
        message['Subject'] = self.SUBJECT
        message['From'] = self.SENDER

        # Set to address header to all recipients if not specified
        if self.HEADER_TO_ADDRESS is None:
            self.HEADER_TO_ADDRESS = ', '.join(self.RECIPIENTS)

        message['To'] = self.HEADER_TO_ADDRESS

        # Encode the text and HTML content and set the character encoding.
        message_body = MIMEMultipart('alternative')
        textpart = MIMEText(
            self.BODY_TEXT.encode(
                self.CHARSET),
            'plain',
            self.CHARSET)
        htmlpart = MIMEText(
            self.BODY_HTML.encode(
                self.CHARSET),
            'html',
            self.CHARSET)

        # Add the text and HTML parts to the child container.
        message_body.attach(textpart)
        message_body.attach(htmlpart)

        # Define the attachment part and encode it using MIMEApplication.
        if self.ATTACHMENT is not None:
            attachment = MIMEApplication(open(self.ATTACHMENT, 'rb').read())
            attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=os.path.basename(self.ATTACHMENT))
            message.attach(attachment)

        message.attach(message_body)
        return message

    def send_email(self):
        client = boto3.client(
            'ses',
            region_name=self.AWS_REGION)
        message = self.create_message()
        try:
            # Provide the contents of the email.
            response = client.send_raw_email(
                Source=self.SENDER,
                Destinations=self.RECIPIENTS,
                RawMessage={
                    'Data': message.as_string(),
                },
                ConfigurationSetName=self.CONFIGURATION_SET
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
