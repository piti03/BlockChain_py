import React,{useState, useEffect} from 'react';
import { API_BASE_URL } from '../config';
import { Button } from 'react-bootstrap';
import Block from './Block';
const PAGE_Range = 3;

 function BlockChain(){
    const [blockchain, setBlockChain] = useState([]);
    const [blockchainLength, setBlockchainLength] = useState(0);
    const fetchBlockChainPage = ({start, end}) => {
        fetch(`${API_BASE_URL}/blockchain/range?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(json => setBlockChain(json))
        
    }

    useEffect(()=>{
        fetchBlockChainPage({start:0, end: PAGE_Range});
        fetch(`${API_BASE_URL}/blockchain`)
            .then(response => response.json())
            .then(json => setBlockchainLength(json));

        fetch(`${API_BASE_URL}/blockchain/length`)
            .then(response => response.json())
            .then(json => setBlockchainLength(json));

    },[]);
    const buttonNumbers = [];
    for (let i =0 ; i < blockchainLength/PAGE_Range; i++){
        buttonNumbers.push(i);
    }


    return (
            <div className='BlockChain'>
                <h3>BlockChain</h3>
                <div>
                      {blockchain.map(block => <Block key={block.hash} block={block}/>)}
                      
                </div>
                <div>
                    
                    {
                    buttonNumbers.map(number => {
                        const start = number * PAGE_Range;
                        const end = (number+1) * PAGE_Range;
                        return(
                            <span key={number} onClick={() => fetchBlockChainPage({start, end})}>
                                <Button size='sm' variant='success'>
                                    {number+1}
                                </Button>{' '}
                            </span>

                        )
                    })}
                </div>
            </div>

    );

}
export default BlockChain;
