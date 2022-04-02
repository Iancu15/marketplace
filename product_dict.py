from threading import Lock


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
            if not quantity_dict:
                return None

            for producer_id in quantity_dict:
                quantity_dict[producer_id] -= 1
                if not quantity_dict[producer_id]:
                    quantity_dict.pop(producer_id)

                return producer_id
