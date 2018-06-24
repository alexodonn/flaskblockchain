from .Block import Block

import time

class Blockchain:
    # difficulty of PoW algorithm
    difficulty = 2

    def __init__(self):
        # data yet to get into blockchain
        self.uncomfirmed_transactions = []
        self.chain = []
        self.genesis()

    # generates a genesis block and appends it to the chain
    def genesis(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.hasher()
        self.chain.append(genesis_block)

    # defines a value of nonce that satisfies our difficulty criteria
    def proof_of_work(self, block):
        block.nonce = 0
        hash = block.hasher()

        while not hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            hash = block.hasher()

        return hash

    @property
    def last_block(self):
        return self.chain[-1]