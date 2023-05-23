from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transactionpool import TransactionPool

def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet() , 'recipient' , 1)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction