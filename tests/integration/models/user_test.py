from models.user import UserModel
from tests.test_base import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', 'password')

            self.assertIsNone(user.find_by_username('test'))
            self.assertIsNone(user.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(user.find_by_username('test'))
            self.assertIsNotNone(user.find_by_id(1))

            user.delete_from_db()
            self.assertIsNone(user.find_by_username('test'))
            self.assertIsNone(user.find_by_id(1))
