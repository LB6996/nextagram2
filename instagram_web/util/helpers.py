import boto3, botocore
from werkzeug.utils import secure_filename
import os, datetime

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
   aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY')
)

def upload_file_to_s3(file, acl="public-read"):
    # file.filename = secure_filename(f"{str(datetime.datetime.now())}_{file.filename}")
    try:
        s3.upload_fileobj(
            file,
            os.getenv('S3_BUCKET_NAME'),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    
    # return "{}{}".format(app.config["S3_LOCATION"], file.filename)
    # return "{}{}".format(os.getenv('S3_LOCATION'), file.filename)
    return file.filename