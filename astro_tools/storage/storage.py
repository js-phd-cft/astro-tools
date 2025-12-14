# src/astro_tools/storage.py
import boto3
import os
from io import BytesIO
from pathlib import Path

class StorageBackend:
    def save_fits(self, hdu_list, path): raise NotImplementedError
    def load_fits(self, path): raise NotImplementedError

class S3Backend(StorageBackend):
    def __init__(self, bucket=None, prefix='', endpoint_url=None):
        self.bucket = bucket or os.getenv('S3_BUCKET')
        self.endpoint_url = endpoint_url or os.getenv('S3_ENDPOINT_URL')
        self.s3 = boto3.client('s3', endpoint_url=self.endpoint_url)
        self.prefix = prefix
    
    def save_fits(self, hdu_list, path):
        buf = BytesIO()
        hdu_list.writeto(buf)
        buf.seek(0)
        
        full_path = f"{self.prefix}/{path}" if self.prefix else path
        self.s3.upload_fileobj(buf, self.bucket, full_path)
        return f"s3://{self.bucket}/{full_path}"
    
    def load_fits(self, path):
        from astropy.io import fits
        buf = BytesIO()
        self.s3.download_fileobj(self.bucket, path, buf)
        buf.seek(0)
        return fits.open(buf)

class FileBackend(StorageBackend):
    def __init__(self, base_path=None):
        self.base = Path(base_path or os.getenv('FILE_STORAGE_PATH', '/scratch/data'))
    
    def save_fits(self, hdu_list, path):
        dest = self.base / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        hdu_list.writeto(dest, overwrite=True)
        return str(dest)
    
    def load_fits(self, path):
        from astropy.io import fits
        return fits.open(self.base / path)

def create_storage(backend='s3', **kwargs):
    if backend == 's3':
        return S3Backend(**kwargs)
    return FileBackend(**kwargs)