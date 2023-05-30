import React, {useState, useEffect} from "react";
import logo from '../assets/logo.png';
import { API_BASE_URL } from "../config";
import BlockChain from "./BlockChain";

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
        <div className="WalletInfo">
          <div>address : {address}</div>
          <div>balance : {balance}</div>
        </div>
        <br/>
        <BlockChain/>
      </div>
  );

}
  
export default App;
