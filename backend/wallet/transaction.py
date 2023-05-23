import uuid
import time
from backend.wallet.wallet import Wallet
class Transaction:
    # Document of exchange ..
    def __init__(self, 
                 sender_wallet=None, recipient=None, amount=None
                 ,id=None, input=None, output=None):
        self.id = id or str(uuid.uuid4())[:8]
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount,
           
        )
        self.input = input or self.create_input(
            sender_wallet, self.output)



    def create_output(self, sender_wallet, recipient, amount):
        # Structure of output
        if amount > sender_wallet.ballance:
            raise Exception('Amount exceeds balance')

        output = {}
        output[recipient] = amount  
        output[sender_wallet.address] = sender_wallet.ballance - amount
        return output   
    

    def create_input(self, sender_wallet, output):
        # Structure of input

        return {
            'timestamp' : time.time_ns(),
            'amount'    : sender_wallet.ballance,
            'address'   : sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature' : sender_wallet.sign(output)
        }
    

    def update(self, sender_wallet, recipient, amount):
        # Update transaction
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance')
        
        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount
        else:
            self.output[recipient] = amount

        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet, self.output)   

    def to_json(self):
        return self.__dict__
    
    @staticmethod
    def from_json(transaction_json):
        return Transaction(**transaction_json)
          
       



    @staticmethod
    def is_valid_transaction(transaction):
        output_total = sum(transaction.output.values())
        if transaction.input['amount'] != output_total:
            raise Exception('Invalid Transaction')
        
        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception('Invalid signature')

        
def main():
    transaction = Transaction(Wallet(),'recipient', 20)
    print(f'transaction.__dict__ : {transaction.__dict__}')
    transaction_json = transaction.to_json()
    restored_transaction = Transaction.from_json(transaction_json)
    print(f'restored_transaction.__dict__ : {restored_transaction.__dict__}')


if __name__ == "__main__":
    main()

    