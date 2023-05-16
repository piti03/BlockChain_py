from backend.blockchain.block import Block
class Blockchain:
    
    # blockchain as a public ledger to storage blocks as each index
    
    def __init__(self):
        self.chain = [Block.genesis()]


    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))
        


    def __repr__(self):
        return f'Blockchain : {self.chain}'      
        




def main():

    blockchain = Blockchain()
    blockchain.add_block('one')   
    blockchain.add_block('two') 
    print(blockchain) 
    print(f'blockchain:__name__{__name__}') 
if __name__ == '__main__':
    main()       