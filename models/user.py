from database import db
from uuid import uuid4

class UserModel(db.Document):
    
    user_id = db.StringField(default=str(uuid4()))
    username = db.StringField()
    password = db.StringField()
    
    def to_json(self):
        return {
            "user_id": self.user_id,
            "user": self.username,
        }

    def creat_user(self):
        user = self.save()
        return user

    @classmethod
    def get_user_by_name(cls, name):
        user = cls.objects(username=name).first()
        return user

    @classmethod
    def get_user_by_userid(cls, user_id):
        user = cls.objects(user_id=user_id).first()
        return user