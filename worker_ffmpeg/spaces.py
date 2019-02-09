import boto3

from . import config

s3_client = None
bucket = None
s3session = None


# Initialize a session using DigitalOcean Spaces.
def init_s3():
    global s3session
    s3session= boto3.session.Session()
    global s3client
    s3client = s3session.client('s3',
                              region_name='ams3',
                              endpoint_url=config.ENDPOINT_URL,
                              aws_access_key_id=config.SPACES_API_KEY,
                              aws_secret_access_key=config.SPACES_API_SECRET)

    global bucket
    bucket = config.BUCKET_NAME


def get_download_url(key):
    return s3client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=60*60)


def upload_file(file_name, upload_path):
    response = s3client.put_object(
        ACL='private',
        Body=open(file_name, 'rb'),
        Bucket=bucket,
        Key=upload_path + '/' + file_name,
    )
    if response:
        return config.ENDPOINT_URL + '/' + bucket + '/' + upload_path + '/' + file_name
