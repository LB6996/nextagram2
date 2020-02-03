from models.base_model import BaseModel
from flask import request
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
import os

class User(UserMixin, BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    profile_image = pw.TextField(default="default_img.jpg")
    private = pw.BooleanField(default=False)
    first_name = pw.CharField(null=True)
    last_name = pw.CharField(null=True)

    def follow(self, idol):
        from models.follows import Follows
        if self.follow_status(idol)==None:
            if idol.private == True:
                return Follows(fan=self.id, idol=idol.id, approved=False).save()
            else:
                return Follows(fan=self.id, idol=idol.id, approved=True).save()
        else:
            return 0

    def unfollow(self, idol):
        from models.follows import Follows
        return Follows.delete().where(Follows.fan == self.id, Follows.idol == idol.id).execute()

    def approve_request(self,fan):
        from models.follows import Follows
        return Follows.update(approved=True).where(Follows.fan==fan.id, Follows.idol==self.id).execute()

    def follow_status(self, idol):
        from models.follows import Follows
        return Follows.get_or_none(Follows.fan == self.id, Follows.idol == idol.id)

    @hybrid_property
    def get_request(self):
        from models.follows import Follows
        return Follows.select().where(Follows.idol==self.id, Follows.approved==False)

    @hybrid_property
    def followers(self):
        from models.follows import Follows
        fans = Follows.select(Follows.fan).where(Follows.idol==self.id, Follows.approved==True)
        return User.select().where(User.id.in_(fans))

    @hybrid_property
    def followings(self):
        from models.follows import Follows
        idols = Follows.select(Follows.idol).where(Follows.fan==self.id, Follows.approved==True)
        return User.select().where(User.id.in_(idols))
    
    @hybrid_property
    def profile_image_url(self):
        return 'http://{}.s3.amazonaws.com/'.format(os.getenv('S3_BUCKET_NAME')) + self.profile_image

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

        # to create new user
        if self.id == None:
            if duplicate_username:
                self.errors.append(f'{self.username} is unvailable!')
            if duplicate_email:
                self.errors.append(f'{self.email} has already been registered1')
            if re.search(password_regex, self.password) == None:
                self.errors.append('Password must have minimum eight characters, at least one letter and one number!1')
            # if self.password != self.cfm_password:
            #     self.errors.append('Password does not match with password confirmatin.')
            else:
                self.password = generate_password_hash(self.password)
        
        # else:
        #     if self.password != None:
        #         if re.search(password_regex, self.password) == None:
        #             self.errors.append('Password must have minimum eight characters, at least one letter and one number!2')
        #         else:
        #             self.password = generate_password_hash(self.password)
        #     elif self.email != None:
        #         if duplicate_email:
        #             self.errors.append(f'{self.email} has already been registered2')

        # for edit info
        else:
            if self.password == None:
            # to handle edit email and name
                if duplicate_email and self.id != duplicate_email.id:
                    self.errors.append(f'{self.email} has already been registered2')
                else:
                    self.password = User.get_by_id(self.id).password 
            
            # to handle edit password
            else:
                # if self.password != User.password:
                if re.search(password_regex, self.password) == None:
                    self.errors.append('Password must have minimum eight characters, at least one letter and one number!2')
                else:
                    self.password = generate_password_hash(self.password)




