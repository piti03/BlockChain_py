import React,{useState, useEffect} from 'react';
import {Button, FormGroup,FormControl} from 'react-bootstrap';
import { API_BASE_URL } from '../config';
import{Link} from'react-router-dom';
import history from '../history';


function ConductTransaction(){
    const [amount, setAmount] = useState(0);
    const [recipient, setRecipient] = useState('');
    const [knownAddresses, setKnownAddresses] = useState([]);

    useEffect(()=>{
        fetch(`${API_BASE_URL}/known_addresses`)
        .then(response => response.json())
        .then(json => setKnownAddresses(json));

    },[]);

    const updatAmount = event => {
        setAmount(event.target.value);
    }
    const updateRecipient = event => {
        setRecipient(Number(event.target.value));
    }
    const submitTransaction = () => {
        fetch(`${API_BASE_URL}/wallet/transact`,
        {
            method: 'POST',
            headers : {'Content-Type':'application/json'},
            body : JSON.stringify({recipient, amount})
        }).then(response => response.json())
          .then(json => {
            console.log('submitTransaction json :', json);
            alert('suceess');
            history.push('/transaction-pool');
          });
          

    }
    
    return(
        <div className='ConductTransaction'>
        <Link to='/'>Home</Link>
        <hr/>
        <h3>conduct transaction</h3>
        <FormGroup>
            <FormControl
            input = 'text'
            placeholder='recipient'
            value={recipient}
            onChange={updateRecipient}
            />
        </FormGroup>
            <hr/>
        <FormGroup>
            <FormControl
            input = 'number'
            placeholder='amount'
            value={amount}
            onChange={updatAmount}
            />
        </FormGroup>
        <div>
           <Button variant='danger' onClick={submitTransaction}>
            submit

           </Button>
        </div>
        <h4>known adresses</h4>
        <div>
            {
                knownAddresses.map((knownAddresses,i) => (
                    <span key={knownAddresses}><u>{knownAddresses}</u>{i !== knownAddresses.length -1 ?', ':''}</span>
                ))
            }
        </div>
    </div>
       
      
      
    );




}
export default ConductTransaction;