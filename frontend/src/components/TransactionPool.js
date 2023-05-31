import React,{useState, useEffect} from 'react';
import{Link} from 'react-router-dom';
import { Button } from 'react-bootstrap';
import Transaction from './Transaction';
import { API_BASE_URL , SECONDS_JS} from '../config';
import history from '../history';

const POLL_INTERVAL = SECONDS_JS * 10;
function TransactionPool(){
const [transactions, setTransactions] = useState([]);

const fetchTransactions = () => {
    fetch(`${API_BASE_URL}/transactions`)
    .then(response => response.json())
    .then(json => {
        console.log('transaction json', json);
        setTransactions(json)});

}

useEffect(()=>{
    fetchTransactions();
    const intervalId = setInterval(fetchTransactions,POLL_INTERVAL);
    return () => clearInterval(intervalId);
    
    
},[]);

const fetchMineBlock = ()=>{
    fetch(`${API_BASE_URL}/blockchain/mine`)
    .then(()=>{
        console.log('success');
        history.pushState('/blockchain')
    });
}





return(
    <div className='TransactionPool'>
        <Link to='/'>Home</Link>
        <hr/>
        <h3>Transaction pool</h3>
        <div>
            {
                    transactions.map(transaction => (
                        <div key={transaction.id}>
                            <hr/>
                            <Transaction transaction={transaction}/>
                        </div>
                    ))
            }
        </div>
            <hr/>
            <Button
            variant='danger'
            onClick={fetchMineBlock}
            >
                mine a block of transactions
            </Button>
    </div>
);




}


export default TransactionPool;