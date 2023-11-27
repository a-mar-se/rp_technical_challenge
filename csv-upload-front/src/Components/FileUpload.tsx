import React from "react";
import axios from "axios";

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

const FileUpload = ({dataTypes}) => {

    const [timeTaken,setTimeTaken] = React.useState<number>(0)
    const [maxDocuments,setMaxDocuments] = React.useState<number>(100)
    const [csvFile, setCsvFile] = React.useState<File | null>(null);
    const [disabled, setDisabled] = React.useState<boolean>(true);
    const [error,setError] = React.useState<string>("")
    const [csvResponse,setCsvResponse] = React.useState<string>("")
    const [recordsErrors,setRecordsErrors] = React.useState([])

    const api_url = "http://localhost:8000/"
    const handleSubmission = async () => {
        if (csvFile !== null){
            const first_time = Date.now()
            let formData = new FormData();
            formData.append('file', csvFile);
            formData.append('table', JSON.stringify(dataTypes));
            try{
                axios.post(api_url + "csv_validation/validate", formData, {
                    headers: {
                      'Content-Type': 'multipart/form-data'
                    }
                }).then(response => {
                    if (response.status === 200){
                        setCsvResponse("All in order on your csv file")
                        setRecordsErrors([])
                    }
                    else{
                        if (response.status === 202){
                        // if (response.data.error !== undefined){
                            // console.log(response)
                            setCsvResponse("Error during validation. Check the wrong values below.")
                            setRecordsErrors(response.data.error)
                        }
                        else{
                            setCsvResponse("API Error during validation: " + response.status)

                        }
                    }
                    const second_time = Date.now()
                    setTimeTaken((second_time - first_time) /1000)
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

    const changeHandler = (e) => {
        const csv = e.target.files[0]
        setCsvFile(csv)
        setDisabled(false)

        setRecordsErrors([])
        setCsvResponse("Use the submit button to check if your data passes validation.")
    }   

    const showMore = () => {
        setMaxDocuments(maxDocuments + 100)
    }

    return(
        <div style={{display:'flex', flexDirection:'column', justifyContent:'center'}}>    
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
            
            {csvResponse !== "" ?
                <div>Time taken to validate: {timeTaken === 0 ? "calculating" : timeTaken} s</div>
                :
                <></>
            }

            {csvResponse !== "" ?
                
                <div>
                    Total number of errors: {timeTaken=== 0 ? "calculating" : recordsErrors.length}
                    {recordsErrors.length > maxDocuments ? 
                        <div>
                            <div>There are more many documents with errors, do you want to show more? Be aware! Browser can break (Uncaught InternalError: too much recursion)</div>
                            <button onClick={showMore}>Show more</button>
                        </div>
                        :
                        <></>
                        }
                    {recordsErrors.map((e,index)=>{
                    if (index > maxDocuments){
                        return <></>
                    }
                    return <div key={"error_" + index}>
                        <div style={{display:'flex', flexDirection:"row"}}>
                            <div className="cell cell-header">entity_id</div>
                            <div className="cell cell-header">data_type</div>
                            <div className="cell cell-header">value</div>
                            <div className="cell cell-header">error description</div>
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
        </div>
    )
}

export default FileUpload;