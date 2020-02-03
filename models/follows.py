from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Follows(BaseModel):
    fan = pw.ForeignKeyField(User, on_delete='CASCADE')
    idol = pw.ForeignKeyField(User, on_delete='CASCADE')
    approved = pw.BooleanField(default=False)