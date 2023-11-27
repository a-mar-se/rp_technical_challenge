import React from "react";
import axios from "axios";
import Modal from 'react-modal';
import AddTypeModal from "./AddTypeModal.js";

interface DataTypeInterface {
    data_type: string,
    description: string,
    extra?: [ExtraValidationInterface],
    basic_data_type?: string
}

interface ExtraValidationInterface {
    type: string,
    value: string
}

const FileUpload = () => {
    const default_data_types:Array<DataTypeInterface> = [
        {data_type:"decimal", description:"Checks if it is a decimal number"},
        {data_type:"integer", description:"Checks if it is an integer number"},
        {data_type:"string", description:"Checks if it is a string"},
        {data_type:"url", description:"Checks if it is a valid url"},
        {data_type:"favicon", description:"Checks if it is a valid url"},
    ];

    const [modalIsOpen, setIsOpen] = React.useState(false);
    const [csvFile, setCsvFile] = React.useState<File | null>(null);
    const [disabled, setDisabled] = React.useState<boolean>(true);
    const [error,setError] = React.useState<string>("")
    const [dataTypes, setDataTypes] = React.useState(default_data_types);
    const [addEnabled, setAddEnabled] = React.useState(false);
    const [newDataType,setNewDataType] = React.useState<string>("")
    const [newDescription,setNewDescription] = React.useState<string>("")
    const [csvResponse,setCsvResponse] = React.useState<string>("")
    const [validationError,setValidationError] = React.useState<string>("")

    const [recordsErrors,setRecordsErrors] = React.useState([])

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
                }).then(response => {
                    if (response.data === ''){
                        console.log("All in order on your csv file")
                        setCsvResponse("All in order on your csv file")
                    }
                    else{
                        if (response.data.error !== undefined){
                            console.log("Error during validation")
                            console.log(response)
                            setCsvResponse("Error during validation")
                            setRecordsErrors(response.data.error)
                        }

                    }
                }).catch(err=>console.error(err));

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


    

    function afterOpenModal() {
    }

    function closeModal() {
        setIsOpen(false);
    }

    const changeHandler = (e) => {
        const csv = e.target.files[0]
        setCsvFile(csv)
        setDisabled(false)

        setCsvResponse("Use the submit button to check if your data passes validation.")
    }


    const update_data_type = (e) => {
        setNewDataType(e.target.value)
    }

    const update_description = (e) => {
        setNewDescription(e.target.value)
    }
    
    

    return(
        <div style={{padding:"5px"}}>
            <h1>CSV data_type validator</h1>
            <h4>Create custom data_types and validations for them. Upload your CSV file with the columns "entity_id", "data_type" and "value" to check if any value is valid as its data_type.</h4>
            <div style={{display:'flex', flexDirection:'column', justifyContent:'center'}}>
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
                                    <>
                                        {element.extra.map(ei=>{
                                            return <div className="cell">{ei.type} : {ei.value}</div>

                                        })}
                                    </>
                                    :
                                    <div className="cell">None</div>
                                }
                            </div>
                        )
                    })}

                    {!modalIsOpen?
                        <div style={{display:'flex', flexDirection:"row"}}>
                            <div className=""><button onClick={()=>setIsOpen(true)}>Add new custom data_type</button></div>
                        </div>
                        :
                        <></>
                    }
                    
                </div>
                <h3>Upload you CSV files here</h3>
                <div style={{display:"flex", flexDirection:"row", justifyContent:'center'}}>
                    <input type="file" name="file" onChange={changeHandler} />
                    <button onClick={handleSubmission} disabled={disabled}>Submit</button>
                </div>
                {error !== "" ?
                    <div>{error}</div>
                    :
                    <></>
                }

                {csvResponse !== "" ?
                    <div>{csvResponse}</div>
                    :
                    <></>
                }
            </div>
            {csvResponse !== "" ?
                <div>{recordsErrors.map(e=>{
                    console.log({e})
                    return <div>
                        <div style={{display:'flex', flexDirection:"row"}}>
                            <div className="cell">entity_id</div>
                            <div className="cell">data_type</div>
                            <div className="cell">value</div>
                            <div className="cell">error description</div>
                        </div>
                        <div style={{display:'flex', flexDirection:"row"}}>
                            <div className="cell">{e.entity_id}</div>
                            <div className="cell">{e.data_type}</div>
                            <div className="cell">{e.value}</div>
                            <div className="cell">{e.error_description}</div>
                        </div>
                    </div>
                })}</div>
                :
                <></>
            }

            <Modal
                isOpen={modalIsOpen}
                onAfterOpen={afterOpenModal}
                onRequestClose={closeModal}
                // style={customStyles}
                contentLabel="Example Modal"
            >
                <AddTypeModal default_data_types={default_data_types} dataTypes={dataTypes} setDataTypes={setDataTypes} closeModal={closeModal} modalIsOpen={modalIsOpen}/>
            </Modal>
        </div>
    )
}

export default FileUpload;