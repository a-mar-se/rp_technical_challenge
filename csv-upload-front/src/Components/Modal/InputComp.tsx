import React, {  } from "react";

const InputComp = ({changeInput, inputValue}) => {
    const changeExtraValue = (e)=>{
        if (e.target.validity.valid){
            changeInput(e.target.value)
        }
    }

    return(
        <input type="text" name="data_type_name" onChange={changeExtraValue} value={inputValue}/>
    )
}

export default InputComp;