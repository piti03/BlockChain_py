import React, {useState, useEffect} from "react";
import logo from '../assets/logo.png';
import { API_BASE_URL } from "../config";
import { Link } from "react-router-dom/cjs/react-router-dom.min";


function App() {
  const[walletInfo, setWalletInfo] = useState({});
  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/info`)
    .then(response => response.json())
    .then(json => setWalletInfo(json));
  }, []);
  const {address, balance} = walletInfo;
    
  



  return (
      <div className="App">
        <img className="logo" src={logo} alt="app_logo"/>
        <h3>BlockChain</h3>
        <br/>
        <Link to="/blockchain">blockchain</Link>
        
        <Link to="/conduct-transaction">transaction</Link>
        <br/>
        <div className="WalletInfo">
          <div>address : {address}</div>
          <div>balance : {balance}</div>
        </div>
      </div>
  );

}
  
export default App;
