import React from "react";
import axelcoin from '../axelcoin.svg'

export default function MPITAxelcounter (props){
    return (
        <div style={{display:'flex', alignItems: "center", gap: "1em"}} >
            <a href="/user">
                <img alt="axelc" style={ {float:'right', margin: '15px'} } width='35' src={axelcoin} />
                <p style={{float:'right', marginTop: '20px', color: "#B328F6"}}>{props.text}</p>
            </a>
        </div>
    );
}