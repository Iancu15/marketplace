"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.setDaemon(kwargs['daemon'])
        self.product_infos = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.id = self.marketplace.register_producer()
        self.name = kwargs['name']

        pass

    def run(self):
        for product_info in self.product_infos:
            (product, quantity, processing_time) = product_info
            for i in range(0, quantity):
                can_i_republish = self.marketplace.publish(self.id, product)
                time.sleep(processing_time)
                if not can_i_republish:
                    time.sleep(self.republish_wait_time)

        pass
