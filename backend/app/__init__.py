import os
import requests
import random
from flask import Flask,jsonify,request
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transactionpool import TransactionPool

app = Flask(__name__)
blockchain = Blockchain()
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)
wallet = Wallet(blockchain)


@app.route('/')
def route_default():
   return 'Welcome to blockchain'



@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())



@app.route('/blockchain/mine')
def route_blockchain_mine():
    
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transactions(blockchain)
    return jsonify(block.to_json())


@app.route('/wallet/transact',methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = transaction_pool.excisting_transaction(wallet.address)
    if transaction:
        transaction.update(
        wallet,
        transaction_data['recipient'],
        transaction_data['amount'])

    else:
        transaction =  Transaction(
        wallet,
        transaction_data['recipient'],
        transaction_data['amount'])

        
    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())  
    
    
@app.route('wallet/info')
def route_wallet_info():
    return jsonify({'address' : wallet.address , 'balance' : wallet.balance})    

                              
    

ROOT_PORT = 5000
PORT = ROOT_PORT
if os.environ.get('PEER') == 'TRUE':
    PORT = random.randint(5001,6000)
    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    result_blockchain = Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print(f'\n-- Successfully synchronized chain')
    except Exception as e:
        print(f'\n-- Error synchronizing chain{e}')

app.run(port=PORT)