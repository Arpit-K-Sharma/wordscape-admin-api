from fastapi import HTTPException, UploadFile
import configparser
import boto3
from botocore.exceptions import ClientError
from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE
import uuid
import asyncio

config = configparser.ConfigParser()
config.read('config.ini')

class FileService:

    @staticmethod
    async def save_uploaded_file(file: UploadFile):
        allowed_extensions = [".pdf", ".jpg", ".jpeg", ".png"]
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            raise HTTPException(
                status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only PDF, JPEG and PNG files are allowed"
            )
        
        s3 = boto3.client(
            's3',
            aws_access_key_id=config['aws']['aws_access_key_id'],
            aws_secret_access_key=config['aws']['aws_secret_access_key'],
            region_name=config['aws']['aws_region_name']
        )
        prefix = config["aws"]["aws_s3_key_prefix"]
        bucket_name = config['aws']['aws_bucket_name']

        async def upload_to_s3(file_content: bytes, file_path: str):
            try:
                s3.put_object(
                    Bucket=bucket_name,
                    Key=file_path,
                    Body=file_content
                )
                print("uploaded")
            except ClientError as e:
                print(f"Error during S3 upload: {e}")
                raise

        try:
            unique_filename = f"{uuid.uuid4()}_{file.filename}"
            file_path = f"{prefix}/{unique_filename}"

            file_content = await file.read()

            asyncio.create_task(upload_to_s3(file_content, file_path))

            print("response")

            return {"filename": unique_filename}

        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            raise HTTPException(status_code=500, detail="Failed to upload file to S3")
