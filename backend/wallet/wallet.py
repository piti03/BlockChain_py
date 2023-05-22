import json
import uuid
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
class Wallet :
    # Individual wallet for a miner
    # Keeps currencies
    # Autorizied the transactions
    def __init__(self):
        self.address = str(uuid.uuid4())[:8]
        self.ballance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(),
            default_backend()
        )
        self.public_key = self.private_key.public_key()

    def sign(self, data):
        # Create signature based on data and private key
        return self.private_key.sign(
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256()))    
    @staticmethod
    def verify(public_key, data, signature):
        # Verify signature based on public key and data
        try:
            public_key.verify(
                signature,
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

def main():
    wallet = Wallet()
    print(f'wallet.__dict__ : {wallet.__dict__}') 
    data = {'foo' : 'bar'}    
    sigature = wallet.sign(data)
    print(f'signature : {sigature}')  
    should_be_valid = Wallet.verify(wallet.public_key, data, sigature)
    should_be_invalid = Wallet.verify(Wallet().public_key, data, sigature)
    print(f'should_be_valid : {should_be_valid}')
    print(f'should_be_invalid : {should_be_invalid}')

if __name__ == "__main__":
    main()    