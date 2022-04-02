from threading import Lock
from threading import Thread
import unittest
from product import Tea
from product import Coffee


class ProductDict:
    def __init__(self):
        self.dict = {}
        self.dict_lock = Lock()

    def put(self, product, producer_id):
        with self.dict_lock:
            if product in self.dict:
                quantity_dict = self.dict[product]
                if producer_id in quantity_dict:
                    quantity_dict[producer_id] += 1
                else:
                    quantity_dict[producer_id] = 1
            else:
                self.dict[product] = {producer_id: 1}

    def remove(self, product):
        with self.dict_lock:
            if product not in self.dict:
                return None

            quantity_dict = self.dict[product]
            for producer_id in quantity_dict:
                quantity_dict[producer_id] -= 1
                producer_id_return = producer_id
                break

            if quantity_dict[producer_id_return] == 0:
                quantity_dict.pop(producer_id_return)

            if not quantity_dict:
                self.dict.pop(product)

            return producer_id_return


class TestProductDict(unittest.TestCase):
    def setUp(self) -> None:
        self.product_dict = ProductDict()
        self.product1 = Tea("Linden", 9, "Herbal")
        self.product2 = Coffee("Indonezia", 1, 5.05, 'MEDIUM')

        def thread_run():
            for i in range(0, 5):
                for j in range(1, 6):
                    self.product_dict.put(self.product1, j)
                    self.product_dict.put(self.product2, j + 1)

        threads = []
        for t in range(0, 10):
            thread = Thread(target=thread_run)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def test_put(self):
        quantity_dict1 = {1: 50, 2: 50, 3: 50, 4: 50, 5: 50}
        quantity_dict2 = {2: 50, 3: 50, 4: 50, 5: 50, 6: 50}
        product_dict = {self.product1: quantity_dict1, self.product2: quantity_dict2}
        self.assertEqual(self.product_dict.dict, product_dict)

    def test_remove(self):
        product_ids1 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        product_ids2 = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        def thread_run():
            for i in range(0, 5):
                for j in range(0, 5):
                    product_id1 = self.product_dict.remove(self.product1)
                    product_ids1[product_id1] += 1
                    product_id2 = self.product_dict.remove(self.product2)
                    product_ids2[product_id2] += 1

        threads = []
        for t in range(0, 10):
            thread = Thread(target=thread_run)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(self.product_dict.dict, {})
        product_ids1_correct = {1: 50, 2: 50, 3: 50, 4: 50, 5: 50}
        product_ids2_correct = {2: 50, 3: 50, 4: 50, 5: 50, 6: 50}
        self.assertEqual(product_ids1, product_ids1_correct)
        self.assertEqual(product_ids2, product_ids2_correct)
        self.assertEqual(self.product_dict.remove(self.product1), None)
