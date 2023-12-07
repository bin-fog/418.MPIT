import React from "react";
import 'primeicons/primeicons.css'

export default function MPITProfileLink () {
    return (
        <div style={{display:'flex', alignItems: "center", gap: "1em", marginRight: "10px"}}>
            <a href="https://a.ru" style={{textDecoration: 'none',color:'#000000', display:'flex', alignItems: "center"}}>
                <p style={{textDecoration: 'none', marginRight: '10px'}}>Пётр И</p>
                <p className="pi pi-user"></p>
            </a>
        </div>
    );
}