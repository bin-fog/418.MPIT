import React from "react";
import { Image } from "primereact/image";
import { Menubar } from "primereact/menubar";
import logo from '../logo.svg'
import MPITAxelcounter from "./MPITAxelcounter";
import MPITProfileLink from "./MPITProfileLink";

export default function MPITMenubar () {

    let items = [
            {
                label: "Главная",
                url: "/"
            },
            {
                label: "Задания"
            },
            {
                label: "Магазин",
                url: "/shop"
            },
            {
                label: "Партнёры"
            },
            {
                label: "Бонусы"
            }
        ];

        let items1 = [
            {
                label: "Главная"
            },
            {
                label: "Задания"
            },
            {
                label: "Магазин"
            },
            {
                label: "Партнёры"
            },
            {
                label: "Бонусы"
            },
            {
                label: "Пётр И"
            }
        ];
    


    let logotlogo = <div style={{display:'flex', alignItems: "center", gap: "1em", marginRight: "40px"}}>
        <Image style={{display: 'inline-block' , margin: '15px'}} alt="Image" width="40" src={logo} />
        <h3 style={{display:'inline-block', whiteSpace: "nowrap", marginBottom: "20px" }}> МПИТ Развитие </h3>
    </div>

    let profile = <div style={{display:'flex', alignItems: "center", gap: "1em", width:"200px",  marginLeft: "40px", marginRight: "10px", overflow: 'hidden'}} >
        <MPITProfileLink />
        <MPITAxelcounter text="50" />
    </div>
    let bar = <Menubar start={logotlogo} model={items} end={profile} style={{overflow: "hidden", display:"flex", whiteSpace: "nowrap"}}
        
    />
    return (
        <div className="card" >
            {bar}
        </div>
    );
}