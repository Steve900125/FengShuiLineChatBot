import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_aws(local_file, bucket_name, s3_file):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file, bucket_name, s3_file)
        print("Upload Successful")
        
        # 構建並返回文件的公開 URL
        location = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        url = f"https://{bucket_name}.s3.{location}.amazonaws.com/{s3_file}"
        print("File URL:", url)
        return url
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None