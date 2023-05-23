import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
 
 
pnconfig= PNConfiguration()
pnconfig.publish_key = 'pub-c-a97cb1a3-9403-48bc-92a7-fd6db53bac5c'
pnconfig.subscribe_key = 'sub-c-2c4d4833-6def-4735-af69-385a2dc80c4e'
pnconfig.uuid = 'sec-c-NmRiNzdhZDQtNDFhMi00OTA2LWI4YzgtMGMxODI2YmI0YTQ5'

pubnub = PubNub(pnconfig)


CHANNELS = {
    'TEST' : 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION' : 'TRANSACTION'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool) :
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
    def message(self, pubnub, message_object):
        print(f'\n-- channel : {message_object.channel} | message :{message_object.message}')
        if message_object.channel == CHANNELS['BLOCK']:
            block =  Block.from_json(message_object.message)    
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print('Successfully replaced chain')
            except Exception as e:
                print(f'\n-- Did not replace chain : {e}')

        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n-- Set the new transaction in transaction pool')






class PubSub():
    # HAndles the publish and subscribe layer of app
    def __init__(self,blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))
       
    def publish(self,channel, message):
        
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self,block):
        # Broadcast block to all nodes
        self.publish(CHANNELS['BLOCK'], block.to_json())


    def broadcast_transaction(self, transaction):
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())    

def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'],{'foo' : 'bar'})


if __name__ == "__main__":
    main()    