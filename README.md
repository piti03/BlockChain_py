**Activate the virtual environment**
'''
   source BlockChain-env/bin/activate
'''
**Install all packages**
'''
   pip3 install -r requirements.txt
**Run tests**
   make sure to activate the virtual environment
'''
   python3 -m pytest backend/tests
'''
**Run the application and API**
'''
make sure to activate the virtual environment
python3 -m backend.app
'''
**Run a peer instance**
'''
make sure to activate the virtual environment
export PEER=TRUE && python3 -m backend.app
'''