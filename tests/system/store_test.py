from models.store import StoreModel
from models.item import ItemModel
from tests.test_base import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test_store')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test_store'))
                self.assertDictEqual(json.loads(response.data), {'id': 1, 'name': 'test_store', 'items': []})

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                response = client.post('/store/test_store')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': "A store with name '{}' already exists.".format('test_store')})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                response = client.delete('/store/test_store')

                self.assertDictEqual(json.loads(response.data), {'message': 'Store deleted'})

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                response = client.get('/store/test_store')

                self.assertDictEqual(json.loads(response.data), {'id': 1, 'name': 'test_store', 'items': []})
                self.assertEqual(response.status_code, 200)

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test_store')

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_name', 399.99, 1).save_to_db()
                response = client.get('/store/test_store')

                self.assertDictEqual(json.loads(response.data),
                                     {'name': 'test_store',
                                      'id': 1,
                                      'items': [
                                          {'name': 'test_name',
                                           'price': 399.99
                                           }
                                      ]})
                self.assertEqual(response.status_code, 200)

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                response = client.get('/stores')

                self.assertDictEqual(json.loads(response.data),
                                     {'stores': [
                                         {'name': 'test_store',
                                          'id': 1,
                                          'items': []
                                          }
                                     ]})
                self.assertEqual(response.status_code, 200)

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_name', 399.99, 1).save_to_db()

                response = client.get('/stores')

                self.assertDictEqual(json.loads(response.data),
                                     {'stores': [
                                         {'name': 'test_store',
                                          'id': 1,
                                          'items': [
                                            {'name': 'test_name',
                                             'price': 399.99
                                             }]
                                          }
                                     ]})
                self.assertEqual(response.status_code, 200)

