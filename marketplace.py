"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import unittest
from threading import Lock
from product_dict import ProductDict
from consumer import Consumer
from producer import Producer
from product import Tea
from product import Coffee


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.next_producer_id = 1
        self.next_producer_id_lock = Lock()
        self.next_cart_id = 1
        self.next_cart_id_lock = Lock()
        self.market_products = ProductDict()
        self.producer_queue_sizes = {}
        self.producer_queue_sizes_lock = Lock()
        self.consumer_carts = {}
        self.consumer_carts_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.next_producer_id_lock:
            curr_producer_id = self.next_producer_id
            self.next_producer_id += 1

        with self.producer_queue_sizes_lock:
            self.producer_queue_sizes[curr_producer_id] = 0

        return curr_producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        with self.producer_queue_sizes_lock:
            if self.producer_queue_sizes[producer_id] >= self.queue_size_per_producer:
                return False

        self.market_products.put(product, producer_id)

        with self.producer_queue_sizes_lock:
            self.producer_queue_sizes[producer_id] += 1

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.next_cart_id_lock:
            curr_cart_id = self.next_cart_id
            self.next_cart_id += 1

        with self.consumer_carts_lock:
            self.consumer_carts[curr_cart_id] = ProductDict()

        return curr_cart_id

    def get_cart(self, cart_id) -> ProductDict:
        with self.consumer_carts_lock:
            return self.consumer_carts[cart_id]

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        producer_id = self.market_products.remove(product)
        if not producer_id:
            return False

        consumer_cart = self.get_cart(cart_id)
        consumer_cart.put(product, producer_id)

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        consumer_cart = self.get_cart(cart_id)
        producer_id = consumer_cart.remove(product)
        self.market_products.put(product, producer_id)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        consumer_cart = self.get_cart(cart_id)
        product_list = []
        for product in consumer_cart.dict:
            quantity_dict = consumer_cart.dict[product]
            for producer_id in quantity_dict:
                quantity = quantity_dict[producer_id]
                for i in range(0, quantity):
                    product_list.append(product)

                with self.producer_queue_sizes_lock:
                    self.producer_queue_sizes[producer_id] -= quantity

        return product_list


class TestMarketplace(unittest.TestCase):
    def setUp(self) -> None:
        self.marketplace = Marketplace(3)
        self.product1 = Tea("Linden", 9, "Linden")
        self.product2 = Coffee("Indonezia", 1, 5.05, 'MEDIUM')

    def test_register_producer(self):
        for i in range(1, 100):
            self.assertEqual(self.marketplace.register_producer(), i)

    def test_publish(self):
        self.marketplace.register_producer()
        self.assertEqual(self.marketplace.publish(1, self.product1), True)
        self.assertEqual(self.marketplace.publish(1, self.product1), True)
        self.assertEqual(self.marketplace.publish(1, self.product2), True)
        self.assertEqual(self.marketplace.producer_queue_sizes[1], 3)
        self.assertEqual(self.marketplace.publish(1, self.product2), False)
        market_products = {self.product1: {1: 2}, self.product2: {1: 1}}
        self.assertEqual(self.marketplace.market_products.dict, market_products)

        self.marketplace.register_producer()
        for i in range(0, 10):
            self.marketplace.publish(2, self.product2)
        market_products[self.product2][2] = 3
        self.assertEqual(self.marketplace.market_products.dict, market_products)

    def test_new_cart(self):
        for i in range(1, 100):
            self.assertEqual(self.marketplace.new_cart(), i)

    def test_get_cart(self):
        pass

    def test_add_to_cart(self):
        self.marketplace.register_producer()
        self.marketplace.register_producer()
        self.marketplace.publish(1, self.product1)
        self.marketplace.publish(2, self.product1)
        self.marketplace.publish(2, self.product2)

        self.marketplace.new_cart()
        self.marketplace.add_to_cart(1, self.product1)
        self.marketplace.add_to_cart(1, self.product1)
        self.marketplace.add_to_cart(1, self.product2)
        self.assertEqual(self.marketplace.market_products.dict, {})
        # cart = {self.product1: {0: 1, 1: 1}, self.product2: {1: 1}}
        # self.assertEqual(self.marketplace.get_cart(0).dict, cart)

    def test_remove_from_cart(self):
        pass

    def test_place_order(self):
        pass
