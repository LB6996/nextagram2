from models.base_model import BaseModel
from models.user import User
from models.image import Image
import peewee as pw

class Donation(BaseModel):
    donor = pw.ForeignKeyField(User, backref='donations', on_delete='CASCADE')
    image = pw.ForeignKeyField(Image, backref='donations', on_delete='CASCADE')
    amount = pw.DecimalField(decimal_places=2,default=0)
