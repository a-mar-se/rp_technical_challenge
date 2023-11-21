const FileUpload = () => {

    const handleSubmission = () => {
        console.log('submitting file');
    }

    const changeHandler = () => {
        console.log('changeHandler');
    }

    return(
        <div>
            <input type="file" name="file" onChange={changeHandler} />
            <div>
                <button onClick={handleSubmission}>Submit</button>
            </div>
        </div>
    )
}

export default FileUpload;