from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property
import os

class Image(BaseModel):
    image_path = pw.TextField()
    user = pw.ForeignKeyField(User, backref='images', on_delete='CASCADE')

    @hybrid_property
    def image_url(self):
        return 'http://{}.s3.amazonaws.com/'.format(os.getenv('S3_BUCKET_NAME')) + self.image_path

