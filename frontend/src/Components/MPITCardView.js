import React from "react";
import { VirtualScroller } from 'primereact/virtualscroller'
import { Card } from "primereact/card";


export default function MPITCard(props) {
    const items = [
        {
            image: "task_sit.png",
            label: "Автономия!"
        },
        {
            image: "task_vk.png",
            label: "Ну да"
        },
        {
            image: "task_ya.png",
            label: "Даааа.... "
        }
    ];

    const itemTemplate = (item, options) => {
        
        return (
            <div style={{ width:'200px', height: '200px'}}>
                <Card style={{borderRadius: '15px', border: 'solid #414141 2px', marginLeft: '6px', marginRight: '6px'}}>
                    <div className="card-div">
                        <img className="card-img" src={'/img/'+item.image}/>
                        <p className="akt_p">{item.label}</p>
                    </div>
                    
                </Card>
            </div>
        );
    };

    return ( 
        <div className="card flex justify-content-center ">
            <p className="default">Задания на сегодня</p>
            <VirtualScroller items={items} itemSize={100} itemTemplate={itemTemplate} orientation="horizontal" className="border-1 surface-border border-round" style={{ marginLeft: '5px', width: '100%', height: '300px' }} />
        </div>
    );
}