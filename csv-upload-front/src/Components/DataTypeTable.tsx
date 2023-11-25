import React from "react";

const DataTypeTable = ({dataTypes, openModal}) => {
    return(
        <div style={{display: "flex", flexDirection: "column", alignItems:'center', borderLeftWidth:"0px", borderRightWidth: "0px", borderColor: "white", borderStyle:"solid"}}>
            <h2>Data_types table</h2>
            <h5>These are the types that are going to be checked on your CSV file. Create new ones if the basics are too basic.</h5>
            <div  style={{display:'flex', flexDirection:"row"}}>
                <div className="cell cell-header">data_types</div>
                <div className="cell cell-header">description</div>
                <div className="cell cell-header">extra validations</div>
            </div>
            {dataTypes.map(element=>{
                return (
                    <div style={{display:'flex', flexDirection:"row"}}>
                        <div className="cell">
                            <div>{element.data_type}</div>
                            {element.basic_data_type ?     
                                <div>Basic type: ({element.basic_data_type})</div>
                                :
                                <></>
                            }
                        </div>
                        <div className="cell">{element.description}</div>
                        {element.extra ?
                            <div className="cell">
                                {element.extra.map(ei=>{
                                    return <div >{ei.type} : {ei.value}</div>

                                })}
                            </div>
                            :
                            <div className="cell">None</div>
                        }
                    </div>
                )
            })}

            <div style={{display:'flex', flexDirection:"row"}}>
                <div className=""><button onClick={openModal}>Add new custom data_type</button></div>
            </div>
        </div>
    )
}

export default DataTypeTable;