import React,{useState, useEffect} from 'react';
import { API_BASE_URL } from '../config';
import Block from './Block';

 function BlockChain(){
    const [blockchain, setBlockChain] = useState([]);

    useEffect(()=>{
        fetch(`${API_BASE_URL}/blockchain`)
        .then(response => response.json())
        .then(json => setBlockChain(json));

    },[]);

    return (
            <div className='BlockChain'>
                <h3>BlockChain</h3>
                <div>
                      {blockchain.map(block => <Block key={block.hash} block={block}/>)}
                      
                </div>
            </div>

    );

}
export default BlockChain;
