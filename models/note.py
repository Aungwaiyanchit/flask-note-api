from database import db
from uuid import uuid4

class NoteModel(db.Document):
    
    note_id = db.StringField(default=str(uuid4()))
    title = db.StringField()
    content = db.StringField()
    posted_by = db.ReferenceField('UserModel')
    
    def to_json(self):
        return {
            "note_id": self.note_id,
            "title": self.title,
            "content": self.content,
            "posted_by": {"user_id": self.posted_by.user_id, "username": self.posted_by.username}
        }

    @classmethod
    def fetch_notes(cls):
        notes = cls.objects()
        return notes

    @classmethod
    def get_notes_by_posted_user(cls, user):
        notes = cls.objects(posted_by=user)
        return notes

    @classmethod
    def get_notes_by_note_id(cls, id):
        notes = cls.objects(note_id=id).first()
        return notes

    @classmethod
    def update_note_by_note_id(cls, id, title, content):
        update_note = cls.objects(note_id=id).update({
            "title": title,
            "content": content
        })
        return update_note

    @classmethod
    def delete_note_by_note_id(cls, id):
        delete_note = cls.objects(note_id=id).delete()
        return delete_note

    def creat_note(self):
        note = self.save()
        return note