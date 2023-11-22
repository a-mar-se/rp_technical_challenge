import React from "react";
import axios from "axios";

const FileUpload = () => {
    const [csvFile, setCsvFile] = React.useState<File | null>(null);
    const [disabled, setDisabled] = React.useState<Boolean>(true);
    const [error,setError] = React.useState<String>("")

    const api_url = "http://localhost:8000/"
    const handleSubmission = async () => {
        if (csvFile !== null){
            console.log('submitting file');
            let formData = new FormData();
            formData.append('file', csvFile);
            try{
                axios.post(api_url + "csv_validation/validate", formData, {
                    headers: {
                      'Content-Type': 'multipart/form-data'
                    }
                })

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
    

    return(
        <div>
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