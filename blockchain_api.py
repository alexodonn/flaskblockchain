# file that launched the api

from model.Block import Block
from model.Blockchain import Blockchain
from flask import Flask, request
import requests
import json
import time

app = Flask(__name__)

# the node's copy of blockchain
blockchain = Blockchain()

# the peers network
peers = set()


# consensus function to make sure every peer has the same chain
def consensus():
    global blockchain

    longest_chain = None
    current_len = len(blockchain)

    for node in peers:
        response = requests.get('http://{}/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.is_valid_proof(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False


def announce_new_block(block):
    for peer in peers:
        url = "http://{}/add_block".format(peer)
        requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))


### API ###
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author", "content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.time()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})


@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    announce_new_block(blockchain.last_block)
    return "Block #{} is mined.".format(result)


@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.uncomfirmed_transactions)


# endpoint to add new peers to the network
@app.route('/add_nodes', methods=['POST'])
def register_new_peers():
    nodes = request.get_json()

    if not nodes:
        return "Invalid data", 400

    for node in nodes:
        peers.add(node)

    return "Success", 201


# endpoint to validate and add a block mined by someone else to the node's chain
@app.route('/add_block', methods=['POST'])
def validate_and_add():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["last_hash"])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


# if __name__ == '__main__':
app.run(debug=True, port=8000)
