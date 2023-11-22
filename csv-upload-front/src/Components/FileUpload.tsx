import React from "react";
import axios from "axios";

const FileUpload = () => {
    const [csvFile, setCsvFile] = React.useState<File | null>(null);
    const [disabled, setDisabled] = React.useState<Boolean>(true);

    const api_url = "http://127.0.0.1:8000/"
    const handleSubmission = async () => {
        if (csvFile !== null){
            console.log('submitting file');
            let formData = new FormData();
            formData.append('file', csvFile);
            await axios.post(api_url + "csv_validation/validate",formData);
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
        </div>
    )
}

export default FileUpload;