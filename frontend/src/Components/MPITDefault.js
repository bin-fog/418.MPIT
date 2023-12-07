import React from "react";

export default function MPITDefault (props){
    return (
        <div className="flex" >
            <h1 className="maindefzag">{props.title}</h1>
            <h3 className="maindefzag">{props.description}</h3>
        </div>
    );
}