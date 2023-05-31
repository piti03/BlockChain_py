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
**install react app**
'''
npx create-react-app frontend
'''
**Create React App requires Node 14 or higher**
**if using the lower version follow steps in linux**
'''
1- sudo apt update
2- sudo npm cache clean -f
3- sudo npm install -g n
4- sudo n latest
'''
**the node command changed location and the old location may be remembered in your current shell.**
**If "node --version" shows the old version then start a new shell, or reset the location hash with:**
**hash -r or rehash**
'''
and finaly run : npx create-react-app frontend
'''
**open frontend directory**
'''
npm run start
'''
**seed the backend with data**
'''
make sure you are in environment
export SEED_DATA && python3 -m backend.app
'''
