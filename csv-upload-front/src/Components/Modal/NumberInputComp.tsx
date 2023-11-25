import React, {  } from "react";

const NumberInputComp = ({changeInput, inputValue}) => {
    const changeExtraValue = (e)=>{
        if (e.target.validity.valid){
            changeInput(e.target.value)
        }
    }

    return(
        <input type="text" name="data_type_name" pattern="[0-9]*" onChange={changeExtraValue} value={inputValue}/>
    )
}

export default NumberInputComp;