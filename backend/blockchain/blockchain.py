from backend.blockchain.block import Block
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



def main():

    blockchain = Blockchain()
    blockchain.add_block('one')   
    blockchain.add_block('two') 
    print(blockchain) 
    print(f'blockchain:__name__{__name__}') 
if __name__ == '__main__':
    main()       