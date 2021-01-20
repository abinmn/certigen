from storages.backends.s3boto3 import S3Boto3Storage


class EmailCsvStorage(S3Boto3Storage):
    bucket_name = 'storage.excelmec.tech'