import React,{useState} from 'react';
import {Button, FormGroup,FormControl} from 'react-bootstrap';
import { API_BASE_URL } from '../config';


function ConductTransaction(){
    const [amount, setAmount] = useState(0);
    const [recipient, setRecipient] = useState('');
    const updatAmount = event => {
        setAmount(event.target.value);
    }
    const updateRecipient = event => {
        setRecipient(Number(event.target.value));
    }
    const submitTransaction = () => {
        fetch(`${API_BASE_URL}/wallet/transact`,{
            method: 'POST',
            headers : {'Content-Type':'application/json'},
            body : JSON.stringify({recipient, amount})
        }).then(response => response.json())
          .then(json => {
            console.log('submitTransactionJson :', json);
            alert()
          })
          

    }
    return(
        <div className='ConductTransaction'>
            <h3>conduct transaction</h3>
            <FormGroup>
                <FormControl
                input = 'text'
                placeholder='recipient'
                value={recipient}
                onChange={updateRecipient}
                />
            </FormGroup>

            <FormGroup>
                <FormControl
                input = 'number'
                placeholder='amount'
                value={amount}
                onChange={updatAmount}
                />
            </FormGroup>
            <div>
               <Button variant='primary' onClick={submitTransaction}>
                submit

               </Button>
            </div>
        </div>
    );




}
export default ConductTransaction;