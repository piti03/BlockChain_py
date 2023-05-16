import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash'     : 'genesis_hash',
    'data'     : [],
    'difficulty' : 3,
    'nonce' : 'genesis_nonce'
}


class Block:
    # a unit of storage which takes place in blockchain
    def __init__(self,timestamp, last_hash, hash, data,difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce


    def __repr__(self):
        return (
            'Block('
            f'timestamp : {self.timestamp},'
            f'last_hash : {self.last_hash},'
            f' hash     : {self.hash},'
            f'data      : {self.data},'
            f'difficulty: {self.difficulty},'
            f'nonce     : {self.nonce})'
               )
               
    

    
    @staticmethod  
    def mine_block(last_block, data):
        # Mine a block based on given last block and data
        timestamp = time.time_ns() # time based on nano seconds
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block,timestamp)
        nonce = 0
        hash = crypto_hash(timestamp,last_hash,data, difficulty, nonce)
        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce+=1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block,timestamp)
            hash = crypto_hash(timestamp,last_hash,data, difficulty, nonce)
        return Block(timestamp, last_hash, hash, data, difficulty, nonce)
    @staticmethod
    def genesis():
        
         return Block(**GENESIS_DATA)  
    
    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        # Calculate the adjusted difficulty according to MINE_RATE.
        # Increase the difficulty for quickly mined blocks.
        # Decrease the difficulty for slowly mined blocks
        if (new_timestamp - last_block.timestamp) < MINE_RATE :
            return last_block.difficulty +1
        if(last_block.difficulty -1) > 0 :
            return last_block.difficulty -1
        return 1
    @staticmethod
    def is_valid_block(last_block,block):
        '''
        Block could be validete by these rules:
            - The block last_hash must be valid.
            - The proof of work must be dominstrated.
            - The difficulty must be adjusted by 1.
            - The block hash must be valid combination of block fields. 
        '''
        if block.last_hash != last_block.hash:
            raise Exception('The block hash must be valid')
        
        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The block difficulty must meet currectly')
        
        if abs(last_block.difficulty - block.difficulty) > 1 :
            raise Exception('The block difficulty must be only adjusted by 1')
        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )
        if block.hash != reconstructed_hash:
            raise Exception('The block hash must have valid combination')

def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block,'foo')
    bad_block.last_hash = 'evil data'
    try:
        Block.is_valid_block(genesis_block,bad_block)
    except Exception as e:
        print(f'is_valid_block : {e}')

    
if __name__ == '__main__':
    main()

    