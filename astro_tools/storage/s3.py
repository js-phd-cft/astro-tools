import boto3
import os
from io import BytesIO

class S3Backend:
       def __init__(self, bucket=None, prefix='', endpoint_url=None, 
                 aws_access_key_id=None, aws_secret_access_key=None):
        """
        Args:
            bucket: S3 bucket (defaults to S3_BUCKET env var)
            endpoint_url: S3 endpoint (defaults to AWS_ENDPOINT_URL env var)
        """
        self.bucket = bucket or os.getenv('S3_BUCKET')
        self.endpoint_url = endpoint_url or os.getenv('AWS_ENDPOINT_URL')
        self.prefix = prefix
        
        self.s3 = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    
    def save_fits(self, hdu_list, path):
        """Save FITS HDUList to S3"""
        buf = BytesIO()
        hdu_list.writeto(buf)
        buf.seek(0)
        
        full_path = f"{self.prefix}/{path}" if self.prefix else path
        self.s3.upload_fileobj(buf, self.bucket, full_path)
        return f"s3://{self.bucket}/{full_path}"