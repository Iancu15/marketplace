"""
This module represents the ProductDict and its test unit class
"""

from threading import Lock
from threading import Thread
import unittest
from tema.product import Tea
from tema.product import Coffee

class ProductDict:
    """
    Class that represents a product dictionary that is thread safe. It's a nested dictionary
    that is a dictionary that has as values other dictionaries. The keys of the external
    dictionary are products and the values, which are the internal dictionaries, contain the
    quantity of the product. The internal dictionary has as values the quantity of the product
    and as key the producer that produced that quantity. The total quantity of said product in
    the dictionary is the sum of the values in the internal dictionary.
    """
    def __init__(self):
        self.dict = {}
        self.dict_lock = Lock()

    def put(self, product, producer_id):
        """
        Adds the product provided by the producer to the dictionary.

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace
        """
        with self.dict_lock:
            if product in self.dict:
                quantity_dict = self.dict[product]

                # daca producatorul avea deja produsul in dictionar, atunci se incrementeaza
                # cantitatea, altfel se adauga producatorul cu cantitatea 0 in dictionarul
                # aferent produsului
                if producer_id in quantity_dict:
                    quantity_dict[producer_id] += 1
                else:
                    quantity_dict[producer_id] = 1
            else:
                # daca produsul nu se afla in dictionare se adauga o mapare pentru acesta
                self.dict[product] = {producer_id: 1}

    def remove(self, product):
        """
        Removes a product from the dictionary.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart


        :returns the producer_id of the producer that had the product which was removed or False.
        If the caller receives False, then it means the product isn't in
        the dictionary.
        """
        with self.dict_lock:
            if product not in self.dict:
                return None

            # pentru un oarecare producator se sustrage o unitate din produsul respectiv
            quantity_dict = self.dict[product]
            for producer_id in quantity_dict:
                quantity_dict[producer_id] -= 1
                producer_id_return = producer_id
                break

            # daca producatorul nu mai are produse de tipul respectiv este eliminat din
            # dictionarul interior
            if quantity_dict[producer_id_return] == 0:
                quantity_dict.pop(producer_id_return)

            # daca produsul are dictionarul aferent gol inseamna ca are cantitatea totala 0
            # si e scos din dictionar
            if not quantity_dict:
                self.dict.pop(product)

            return producer_id_return


class TestProductDict(unittest.TestCase):
    """
    Class that represents the test unit class of the class ProductDict
    """
    def setUp(self) -> None:
        self.product_dict = ProductDict()
        self.product1 = Tea("Linden", 9, "Herbal")
        self.product2 = Coffee("Indonezia", 1, 5.05, 'MEDIUM')

        def thread_run():
            for _ in range(0, 5):
                for j in range(1, 6):
                    self.product_dict.put(self.product1, j)
                    self.product_dict.put(self.product2, j + 1)

        threads = []
        for _ in range(0, 10):
            thread = Thread(target=thread_run)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def test_put(self):
        """
        Unit test that tests the functionality of the function put
        """
        quantity_dict1 = {1: 50, 2: 50, 3: 50, 4: 50, 5: 50}
        quantity_dict2 = {2: 50, 3: 50, 4: 50, 5: 50, 6: 50}
        product_dict = {self.product1: quantity_dict1, self.product2: quantity_dict2}
        self.assertEqual(self.product_dict.dict, product_dict)

    def test_remove(self):
        """
        Unit test that tests the functionality of the function remove
        """
        product_ids1 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        product_ids2 = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        def thread_run():
            for _ in range(0, 5):
                for _ in range(0, 5):
                    product_id1 = self.product_dict.remove(self.product1)
                    product_ids1[product_id1] += 1
                    product_id2 = self.product_dict.remove(self.product2)
                    product_ids2[product_id2] += 1

        threads = []
        for _ in range(0, 10):
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
