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

    @property
    def last_block(self):
        return self.chain[-1]

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

    # check if a block_hash is valid and satisfies our difficulty criteria
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.hasher())

    # adds a block to the chain after verification
    def add_block(self, block, proof):
        last_hash = self.last_block.hash

        if last_hash != block.last_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def add_new_transaction(self, transaction):
        self.uncomfirmed_transactions.append(transaction)

    # serves as an interface to add the per transactions to the blockchain
    def mine(self):
        if not self.uncomfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.uncomfirmed_transactions,
                          timestamp=time.time(),
                          last_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.uncomfirmed_transactions = [0]
        return new_block.index
