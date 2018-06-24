from hashlib import sha256
import json


class Block:
    def __init__(self, index, transactions, timestamp, last_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.last_hash = last_hash

    def hasher(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()



