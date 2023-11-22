import React from "react";
import axios from "axios";

const FileUpload = () => {
    const default_data_types = [
        {data_type:"number", description:"Checks if it is a number"},
        {data_type:"string", description:"Checks if it is a string"},
        {data_type:"url", description:"Checks if it is a valid url"},
    ];

    const [csvFile, setCsvFile] = React.useState<File | null>(null);
    const [disabled, setDisabled] = React.useState<boolean>(true);
    const [error,setError] = React.useState<string>("")
    const [dataTypes, setDataTypes] = React.useState(default_data_types);
    const [addEnabled, setAddEnabled] = React.useState(false);
    const [newDataType,setNewDataType] = React.useState<string>("")
    const [newDescription,setNewDescription] = React.useState<string>("")

    const api_url = "http://localhost:8000/"
    const handleSubmission = async () => {
        if (csvFile !== null){
            console.log('submitting file');
            let formData = new FormData();
            formData.append('file', csvFile);
            formData.append('table', JSON.stringify(dataTypes));
            try{
                axios.post(api_url + "csv_validation/validate", formData, {
                    headers: {
                      'Content-Type': 'multipart/form-data'
                    }
                }).then(response => response).catch(err=>console.error(err));

                // const val = await axios.post(api_url + "csv_validation/validate",{
                //     file: "fillli",
                //     headers: {
                //         "Access-Control-Allow-Origin": "*",
                //         "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
                //     }

                // }).then(response => response).catch(err=>console.error(err));
            }
            catch(error){
                console.log({error})
                setError("Error uploading file to the api")
            }
        }
        else{
            alert("Please provide a CSV file")
        }
    }

    const changeHandler = (e) => {
        const csv = e.target.files[0]
        setCsvFile(csv)
        setDisabled(false)
    }

    const add_custom_row = () => {
        setAddEnabled(true)
    }

    const save_new_data_type = () => {
        setAddEnabled(false);
        const updated_data_types = [...dataTypes,{data_type: newDataType, description: newDescription}];
        setDataTypes(updated_data_types);
        setNewDataType("");
        setNewDescription("");
    }

    const update_data_type = (e) => {
        setNewDataType(e.target.value)
    }

    const update_description = (e) => {
        setNewDescription(e.target.value)
    }
    

    return(
        <div>
            <div>
                <div style={{display:'flex', flexDirection:"row"}}>
                    <div className="cell">data_types</div>
                    <div className="cell">description</div>
                </div>
                {dataTypes.map(element=>{
                    return (
                        <div style={{display:'flex', flexDirection:"row"}}>
                            <div className="cell">{element.data_type}</div>
                            <div className="cell">{element.description}</div>
                        </div>
                    )
                })}
                {addEnabled ?
                    <div style={{display:'flex', flexDirection:"row"}}>
                        <input className="cell" type="string" onChange={update_data_type} placeholder="Data_type_name"/>
                        <input className="cell"  onChange={update_description} placeholder="Description"/>
                    </div>
                    :
                    <></>
                }
                {addEnabled ?
                    <div style={{display:'flex', flexDirection:"row"}}>
                        <div className="cell"><button onClick={()=>save_new_data_type()}>Save new data_type</button></div>
                    </div>
                    :
                    <div style={{display:'flex', flexDirection:"row"}}>
                        <div className="cell"><button onClick={()=>add_custom_row()}>Add new data_type</button></div>
                    </div>
                }
                
            </div>
            <input type="file" name="file" onChange={changeHandler} />
            <div>
                <button onClick={handleSubmission} disabled={disabled}>Submit</button>
            </div>
            {error !== "" ?
                <div>{error}</div>
                :
                <></>
            }
        </div>
    )
}

export default FileUpload;