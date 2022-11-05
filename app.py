from flask import Flask, jsonify
from flask_restful import Api
from flask_uuid import FlaskUUID
from database import db

from resources.user import Users
from resources.note import Notes, Note, DeleteNote, UpdateNote

app = Flask(__name__)
# app.config["MONGODB_SETTINGS"] = {
#     "db": "notes",
#     "host": "localhost",
#     "port": 27017
# }
app.config["MONGODB_HOST"] = 'mongodb+srv://awyc:adan3433@cluster0.u4qke.mongodb.net/notes?retryWrites=true&w=majority'
api = Api(app)
FlaskUUID(app)


api.add_resource(Notes, "/notes")
api.add_resource(Note, "/notes/getByUser")
api.add_resource(UpdateNote, "/notes/update")
api.add_resource(DeleteNote, "/notes/delete")

api.add_resource(Users, "/users")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)