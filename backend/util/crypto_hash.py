import hashlib
import json

def crypto_hash(*args):
    '''
    Returns a SHA-256 of given data
    '''
    stringified_args = sorted(map(lambda data : json.dumps(data),args))  
    # By that you can hash a list, number, string or so .
    # While without you only can hash a string parameter .
    joined_data = ''.join(stringified_args) 
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

   
    


def main():
    print(f"crypto_hash('one',2,[]) : {crypto_hash('one',2,[3])}")
    print(f"crypto_hash(2,'one,[]) : {crypto_hash(2,'one',[3])}")

if __name__ == "__main__":
    main()    