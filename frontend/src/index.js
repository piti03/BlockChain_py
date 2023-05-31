import React from 'react';
import  ReactDOM  from 'react-dom';
import {Route, Switch,Router} from 'react-router-dom';
import{createBrowserHistory} from 'history';
import BlockChain from './components/BlockChain';
import ConductTransaction from './components/ConductTransaction';
import './index.css';
import App from './components/App';

ReactDOM.render(
  <Router history={createBrowserHistory()}>
    <Switch>
        <Route path='/' exact component={App}/>
        <Route path='/blockchain' component={BlockChain}/>
        <Route path='/condust-transaction' component={ConductTransaction}/> 
    </Switch>
  </Router>,
  document.getElementById('root')
);


