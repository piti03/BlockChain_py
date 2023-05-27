from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT
class Blockchain:
    
    # blockchain as a public ledger to storage blocks as each index
    
    def __init__(self):
        self.chain = [Block.genesis()]


    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))
        


    def __repr__(self):
        return f'Blockchain : {self.chain}' 


    def replace_chain(self,chain):
                # Chain could be replaced by this rules:
                     # - The new chain be longer than local one
                     # - The new chain must be formatted correctly
        if len(chain) <= len(self.chain) :
            raise Exception('Cannot replace.New chain must be longer') 
        try:
            Blockchain.is_valid_chain(chain)           
        except Exception as e:
            raise Exception('Cannot replace.New chain must formatted correctly')
        
        self.chain = chain
    def to_json(self):
        # Serialize the blockchain data
        return list(map(lambda block : block.to_json(), self.chain))


    @staticmethod
    def from_json(chain_json):
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json : Block.from_json(block_json),chain_json))
        return blockchain



        
    @staticmethod
    def is_valid_chain(chain):
                 #   A valid chain must have these rules:
                 #       - Chain must starts by genesis block
                 #       - The mined block must formatted correctly
        
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')
     
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)    

    @staticmethod
    def is_valid_transaction_chain(chain):
        # Rules of chain :
            # Each transaction must only appear once in the chain.
            # Only one mining reward per block.
            # Each transaction must be valid.
        transaction_ids = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False
            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)
                if transaction.id  in transaction_ids:
                    raise Exception(f'Transaction{transaction.id} is not unique')
                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception('There can be only one mining reward per block'\
                                        f'CHECK Block hash {block.hash}')
                    has_mining_reward = True
                else:    
                    Transaction.is_valid_transaction(transaction)
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address'])
                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction{transaction.id} has invalid input amount')

                


def main():

    blockchain = Blockchain()
    blockchain.add_block('one')   
    blockchain.add_block('two') 
    print(blockchain) 
    print(f'blockchain:__name__{__name__}') 
if __name__ == '__main__':
    main()       