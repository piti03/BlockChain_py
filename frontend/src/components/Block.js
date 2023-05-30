import React,{useState} from "react";
import {MILISECONDS_PY } from "../config";
import Transaction from "./Transaction";
import {Button} from 'react-bootstrap';


function ToggleTransactionDisplay({block}){
    const [displayTransaction, setDisplayTransaction] = useState(false);
    const {data} = block;
    const toggleDisplayTransaction = ()=>{
        setDisplayTransaction(!displayTransaction);
    }

    if (displayTransaction){
        return(
            <div>
               {
                    data.map(transaction => (
                      <div key={transaction.id}>
                       <hr/>
                        <Transaction transaction={transaction}/>
                      </div>
                     ))
                }
                <br/>
                <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>
                    Show less

                </Button>
            </div>
        );
    }
    return(
        <div>
            <br/>
            <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>
                Show More
            </Button>
        </div>
       
    );





}



function Block({block}){
    const {timestamp, hash} = block;
    const hashDisplay = `${hash.substring(0,12)}...`;
    const timestampDisplay = new Date(timestamp / MILISECONDS_PY).toLocaleString();


    return (

        <div className="Block">
            <div>HASH : {hashDisplay}</div>
              <div>TIMESTAMP : {timestampDisplay}</div>
              <ToggleTransactionDisplay block={block} />
              
        </div>



    );


}



export default Block;