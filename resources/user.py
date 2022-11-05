from flask_restful import Resource, reqparse
from models.user import UserModel

class Users(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="username cannot be blank."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="password cannot be blank."
    )

    def get(self):
        users = UserModel.objects()
        return { "users": [user.to_json() for user in users]}

    def post(self):
        data = Users.parser.parse_args()
        old_user = UserModel.get_user_by_name(data["username"])
        if old_user is not None:
            return { "message": "user already exists." } , 409
        user = UserModel(username=data["username"], password=data["password"])
        user.creat_user()

        return { "message": "user successfully created." }, 201


# class User(Resource):
#     def get(self, username):
#         user = UserModel.get_user_by_name(username)
#         return {
#             "users"
#         }