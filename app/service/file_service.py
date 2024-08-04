import os
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile
import boto3
from botocore.exceptions import ClientError
from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE
import uuid
import asyncio

# Load environment variables from .env file
load_dotenv()

class FileService:

    @staticmethod
    async def save_uploaded_file(file: UploadFile):
        allowed_extensions = [".pdf", ".jpg", ".jpeg", ".png"]
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            raise HTTPException(
                status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only PDF, JPEG, and PNG files are allowed"
            )
        
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION_NAME')
        )
        prefix = os.getenv("AWS_S3_KEY_PREFIX")
        bucket_name = os.getenv('AWS_BUCKET_NAME')

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
