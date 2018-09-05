from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    """
    This resource allows user to register by sending a POST request
    with username and password
    """

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank!")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank!")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with such username already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'Successfully created'}, 201


class UserDelete(Resource):

    """
    This resource allows user to delete by sending a DELETE request
    with username and password
    """

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank!")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank!")

    def delete(self):
        data = UserDelete.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user:
            user.delete_from_db()

            return {'message': 'Successfully removed user'}, 200

        return {'message': 'User with such username does not exist'}, 400
