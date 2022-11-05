from models.user import UserModel
from models.note import NoteModel
from flask_restful import Resource, reqparse

class Notes(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "title",
        type=str,
        required=True,
        help="title cannot be blank."
    )
    parser.add_argument(
        "content",
        type=str,
        required=True,
        help="content cannot be blank."
    )
    parser.add_argument(
        "posted_by",
        type=str,
        required=True,
        help="posted_by cannot be blank."
    )

    def get(self):
        notes = NoteModel.fetch_notes()
        return { "note": [note.to_json() for note in notes ]}

    def post(self):
        data = Notes.parser.parse_args()
        user = UserModel.get_user_by_userid(data["posted_by"])
        if user is None:
            return { "message": "invalid user_id or user not found." }, 404
        new_note = NoteModel(title=data["title"], content=data["content"], posted_by=user)
        new_note.creat_note()
        return { 
            "message": "note successfully created.",
            "note": new_note.to_json()
         }, 201


class Note(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "user_id",
        type=str,
        required=True,
        help="user_id cannot be blank."
    )

    def post(self):
        data = Note.parser.parse_args()

        user = UserModel.get_user_by_userid(data["user_id"])
        notes = NoteModel.get_notes_by_posted_user(user=user)
        return {
            "notes": [note.to_json() for note in notes]
        }

class DeleteNote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "note_id",
        type=str,
        required=True,
        help="note_id cannot be blank."
    )

    def post(self):
        data = DeleteNote.parser.parse_args()

        note = NoteModel.get_notes_by_note_id(data["note_id"])
        if note is None:
            return { "message": "note with this id not found." }, 404
        try:
            NoteModel.delete_note_by_note_id(note.note_id)
        except:
            return { "message": "an error occured." }, 500
        return { "message": "note successfully deleted." }

class UpdateNote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "note_id",
        type=str,
        required=True,
        help="note_id cannot be blank."
    )
    parser.add_argument(
        "title",
        type=str,
        required=True,
        help="title cannot be blank."
    )
    parser.add_argument(
        "content",
        type=str,
        required=True,
        help="content cannot be blank."
    )

    def post(self):
        data = UpdateNote.parser.parse_args()

        note = NoteModel.get_notes_by_note_id(data["note_id"])
        if note is None:
            return { "message": "note not found with this id."}, 404
        update = {
            "title": data["title"],
            "content": data["content"]
        }
        try:
            note.update(**update)
        except BaseException as err:
            print(err)
            return { "message": "an error occured." }, 500
        return { "message": "note successfully updated." }