# class that defines a block
from hashlib import sha256
import json


class Block:
    def __init__(self, index, transactions, timestamp):
        self.index = []
        self.transactions = transactions
        self.timestamp = timestamp

    def hasher(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()



