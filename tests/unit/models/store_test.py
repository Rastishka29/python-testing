from models.store import StoreModel
from tests.unit.test_unit_base import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_item(self):
        item = StoreModel('test')

        self.assertEqual(item.name, 'test',
                         "The name of the item after creation does not equal the constructor argument.")
