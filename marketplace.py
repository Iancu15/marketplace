"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import logging
import time
import unittest
from threading import Lock
from logging.handlers import RotatingFileHandler
from tema.product_dict import ProductDict
from tema.product import Tea
from tema.product import Coffee


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

        # id-ul urmatorului producator, se incepe numaratoarea de la 1
        self.next_producer_id = 1
        self.next_producer_id_lock = Lock()

        # id-ul urmatorului cos, se incepe numaratoarea de la 1
        self.next_cart_id = 1
        self.next_cart_id_lock = Lock()

        # produsele disponibile pe piata plasate de producatori
        self.market_products = ProductDict()

        # dictionar cu dimensiunea cozilor fiecarui producator
        self.producer_queue_sizes = {}
        self.producer_queue_sizes_lock = Lock()

        # dictionar ce mapeaza id-ul cosului la continutul cosului
        self.consumer_carts = {}
        self.consumer_carts_lock = Lock()
        handler = RotatingFileHandler(
            'marketplace.log',
            mode='w',
            maxBytes=1000000,
            backupCount=1000,
            delay=True
        )

        logging.basicConfig(
            handlers=[handler],
            level=logging.INFO,
            format='%(asctime)s %(levelname)s : %(message)s'
        )

        logging.Formatter.converter = time.gmtime

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        logging.info('Entering register_producer')
        with self.next_producer_id_lock:
            curr_producer_id = self.next_producer_id
            self.next_producer_id += 1

        with self.producer_queue_sizes_lock:
            self.producer_queue_sizes[curr_producer_id] = 0

        logging.info('Leaving register_producer')
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
        logging.info('Entering publish with producer_id=%d product=%s', producer_id, repr(product))

        # daca coada producatorului e plina se intoarce False
        with self.producer_queue_sizes_lock:
            if self.producer_queue_sizes[producer_id] >= self.queue_size_per_producer:
                logging.info('Leaving publish')
                return False

        # se adauga produsul pe piata
        self.market_products.put(product, producer_id)

        with self.producer_queue_sizes_lock:
            self.producer_queue_sizes[producer_id] += 1

        logging.info('Leaving publish')
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        logging.info('Entering new_cart')
        with self.next_cart_id_lock:
            curr_cart_id = self.next_cart_id
            self.next_cart_id += 1


        # cosul contine produse etichetate dupa producator asa ca folosesc un ProductDict
        with self.consumer_carts_lock:
            self.consumer_carts[curr_cart_id] = ProductDict()

        logging.info('Leaving new_cart')
        return curr_cart_id

    def get_cart(self, cart_id) -> ProductDict:
        """
        Returns the cart mapped to the id

        :type cart_id: Int
        :param cart_id: id cart

        :returns a ProductDict that has the content of the cart
        """
        logging.info('Entering get_cart with cart_id=%d', cart_id)
        with self.consumer_carts_lock:
            logging.info('Leaving get_cart')
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
        logging.info('Entering add_to_cart with cart_id=%d product=%s', cart_id, repr(product))
        producer_id = self.market_products.remove(product)

        # produsul nu exista pe piata daca in cos nu e mapat la niciun producer_id
        if not producer_id:
            logging.info('Leaving add_to_cart')
            return False

        consumer_cart = self.get_cart(cart_id)
        consumer_cart.put(product, producer_id)

        logging.info('Leaving add_to_cart')
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        log_message = 'Entering remove_from_cart with cart_id=%d product=%s'
        logging.info(log_message, cart_id, repr(product))
        consumer_cart = self.get_cart(cart_id)
        producer_id = consumer_cart.remove(product)

        # adaug produsul scos din cos inapoi pe piata ca a redevenit disponibil
        self.market_products.put(product, producer_id)
        logging.info('Leaving remove_from_cart')

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        logging.info('Entering place_order with cart_id=%d', cart_id)
        consumer_cart = self.get_cart(cart_id)
        product_list = []
        for product in consumer_cart.dict:
            quantity_dict = consumer_cart.dict[product]

            # pentru fiecare producator mapat la produsul respectiv in cos
            # se ia cantitatea din cos a produsului data de producatorul respectiv
            # si se adauga unul cate unul produsul in lista
            for producer_id in quantity_dict:
                quantity = quantity_dict[producer_id]
                for _ in range(0, quantity):
                    product_list.append(product)

                # se scade din coada producatorului cantitatea ce urmeaza a fi cumparata
                with self.producer_queue_sizes_lock:
                    self.producer_queue_sizes[producer_id] -= quantity

        logging.info('Leaving place_order')
        return product_list


class TestMarketplace(unittest.TestCase):
    """
    Class that represents the test unit class of the class Marketplace
    """
    def setUp(self) -> None:
        self.marketplace = Marketplace(3)
        self.product1 = Tea("Linden", 9, "Linden")
        self.product2 = Coffee("Indonezia", 1, 5.05, 'MEDIUM')

    def test_register_producer(self):
        """
        Unit test that tests the functionality of the function register_producer
        """
        for _ in range(1, 100):
            self.assertEqual(self.marketplace.register_producer(), i)

    def test_publish(self):
        """
        Unit test that tests the functionality of the function publish
        """
        self.marketplace.register_producer()
        self.assertEqual(self.marketplace.publish(1, self.product1), True)
        self.assertEqual(self.marketplace.publish(1, self.product1), True)
        self.assertEqual(self.marketplace.publish(1, self.product2), True)
        self.assertEqual(self.marketplace.producer_queue_sizes[1], 3)

        self.assertEqual(self.marketplace.publish(1, self.product2), False)
        self.assertEqual(self.marketplace.producer_queue_sizes[1], 3)
        market_products = {self.product1: {1: 2}, self.product2: {1: 1}}
        self.assertEqual(self.marketplace.market_products.dict, market_products)

        self.marketplace.register_producer()
        for _ in range(0, 10):
            self.marketplace.publish(2, self.product2)

        market_products[self.product2][2] = 3
        self.assertEqual(self.marketplace.market_products.dict, market_products)

    def test_new_cart(self):
        """
        Unit test that tests the functionality of the function new_cart
        """
        for i in range(1, 100):
            self.assertEqual(self.marketplace.new_cart(), i)

    def test_get_cart(self):
        """
        Unit test that tests the functionality of the function get_cart
        """
        self.marketplace.new_cart()
        self.assertEqual(self.marketplace.get_cart(1).dict, {})
        self.marketplace.register_producer()
        for i in range(1, 4):
            self.marketplace.publish(1, self.product1)
            self.marketplace.add_to_cart(1, self.product1)
            cart = {self.product1: {1: i}}
            self.assertEqual(self.marketplace.get_cart(1).dict, cart)

    def test_add_to_cart(self):
        """
        Unit test that tests the functionality of the function add_to_cart
        """
        self.marketplace.register_producer()
        self.marketplace.register_producer()
        self.marketplace.publish(1, self.product1)
        self.marketplace.publish(2, self.product1)
        self.marketplace.publish(2, self.product2)

        self.marketplace.new_cart()
        self.marketplace.add_to_cart(1, self.product1)
        self.marketplace.add_to_cart(1, self.product1)
        cart = {self.product1: {1: 1, 2: 1}}
        self.assertEqual(self.marketplace.get_cart(1).dict, cart)

        self.marketplace.add_to_cart(1, self.product2)
        self.assertEqual(self.marketplace.market_products.dict, {})
        cart = {self.product1: {1: 1, 2: 1}, self.product2: {2: 1}}
        self.assertEqual(self.marketplace.get_cart(1).dict, cart)

    def fill_cart(self):
        """
        Function that fills a cart with some products, used in testing remove_from_cart and
        place_order
        """
        self.marketplace.register_producer()
        self.marketplace.register_producer()
        self.marketplace.new_cart()
        for _ in range(1, 4):
            self.marketplace.publish(1, self.product1)
            self.marketplace.publish(2, self.product2)
            self.marketplace.add_to_cart(1, self.product2)
            self.marketplace.add_to_cart(1, self.product1)

    def test_remove_from_cart(self):
        """
        Unit test that tests the functionality of the function remove_from_cart
        """
        self.fill_cart()
        for i in range(0, 3):
            cart = {self.product1: {1: 3 - i}, self.product2: {2: 3}}
            self.assertEqual(self.marketplace.get_cart(1).dict, cart)
            self.marketplace.remove_from_cart(1, self.product1)
            market_products = {self.product1: {1: i + 1}}
            self.assertEqual(self.marketplace.market_products.dict, market_products)

        for i in range(0, 3):
            cart = {self.product2: {2: 3 - i}}
            self.assertEqual(self.marketplace.get_cart(1).dict, cart)
            self.marketplace.remove_from_cart(1, self.product2)
            market_products = {self.product1: {1: 3}, self.product2: {2: i + 1}}
            self.assertEqual(self.marketplace.market_products.dict, market_products)

        self.assertEqual(self.marketplace.get_cart(1).dict, {})

    def test_place_order(self):
        """
        Unit test that tests the functionality of the function place_order
        """
        self.fill_cart()
        self.marketplace.remove_from_cart(1, self.product1)
        self.marketplace.remove_from_cart(1, self.product2)
        products = self.marketplace.place_order(1)
        product1_count = 0
        product2_count = 0
        for product in products:
            if product == self.product1:
                product1_count += 1

            if product == self.product2:
                product2_count += 1

        self.assertEqual(product1_count, 2)
        self.assertEqual(product2_count, 2)
        market_products = {self.product1: {1: 1}, self.product2: {2: 1}}
        self.assertEqual(self.marketplace.market_products.dict, market_products)
        self.assertEqual(self.marketplace.producer_queue_sizes[1], 1)
        self.assertEqual(self.marketplace.producer_queue_sizes[2], 1)
