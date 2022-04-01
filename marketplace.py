"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock
import queue


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
        self.next_producer_id = 0
        self.curr_producer_id_lock = Lock()
        self.next_cart_id = 0
        self.new_cart_id_lock = Lock()
        self.market_products = {}
        self.market_product_lock = Lock()
        self.producer_queue_sizes = {}
        self.producer_queue_sizes_lock = Lock()
        self.consumer_carts = {}
        self.consumer_carts_lock = Lock()

        pass

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.curr_producer_id_lock:
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
        # with self.producer_queue_sizes_lock:
        #     if self.producer_queue_sizes[producer_id] >= self.queue_size_per_producer:
        #         return False
        #
        # with self.market_product_lock:
        #     if product in self.market_products:
        #         product_quantity = self.market_products[product]
        #         if producer_id in product_quantity:
        #             product_quantity[producer_id] += 1
        #         else:
        #             product_quantity[producer_id] = 1
        #     else:
        #         self.market_products[product] = {producer_id: 1}
        #
        # with self.producer_queue_sizes_lock:
        #     self.producer_queue_sizes[producer_id] += 1

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.new_cart_id_lock:
            curr_cart_id = self.next_cart_id
            self.next_cart_id += 1

        with self.consumer_carts_lock:
            self.consumer_carts[curr_cart_id] = {}

        return curr_cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # with self.market_products:
        #     if product not in self.market_products:
        #         return False
        #
        #     product_quantity = self.market_products[product]
        #     if not product_quantity:
        #         return False
        #
        #     for producer_id in product_quantity:
        #         product_quantity[producer_id] -= 1
        #         break
        #
        # with self.consumer_carts_lock:
        #     consumer_cart = self.consumer_carts[cart_id]
        #
        # if product in consumer_cart:
        #     product_quantity = self.market_products[product]
        #     consumer_cart[product][0] += 1
        # else:
        #     consumer_cart[product] = [1,]

        pass

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        pass

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        pass
