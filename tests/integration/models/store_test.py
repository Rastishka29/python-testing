from models.store import StoreModel
from models.item import ItemModel
from tests.test_base import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [],
                             "Store items are not empty even though no items were added")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 399.99, 1)

            store.save_to_db()  # you need to initialize store prior to the item, because item needs a store
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_json(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 399.99, 1)

            store.save_to_db()  # you need to initialize store prior to the item, because item needs a store
            item.save_to_db()

            expected = {
                'name': 'test',
                'id': 1,
                'items': [{
                    'name': item.name,
                    'price': item.price,
                           }]
            }

            self.assertDictEqual(store.json(), expected,
                                 "The returned JSON for created store does not match the constructor"
                                 )






