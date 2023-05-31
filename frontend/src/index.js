import React from 'react';
import  ReactDOM  from 'react-dom';
import {Route, Switch,Router} from 'react-router-dom';
import history from './history';
import BlockChain from './components/BlockChain';
import ConductTransaction from './components/ConductTransaction';
import TransactionPool from './components/TransactionPool';
import './index.css';
import App from './components/App';

ReactDOM.render(
  <Router history={history}>
    <Switch>
        <Route path='/' exact component={App}/>
        <Route path='/blockchain' component={BlockChain}/>
        <Route path='/condust-transaction' component={ConductTransaction}/> 
        <Route path='/transaction-pool' component={TransactionPool}/>
    </Switch>
  </Router>,
  document.getElementById('root')
);


