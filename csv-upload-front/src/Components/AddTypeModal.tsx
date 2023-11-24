import React, { useEffect, useState } from "react";
import axios from "axios";
import Modal from 'react-modal';
import Select from 'react-select';

interface OptionInterface {
    label: string,
    value: string
}

interface ExtraValidationInterface {
    type: string,
    value: string
}

const AddTypeModal = ({default_data_types, dataTypes, setDataTypes, closeModal}) => {
    const extra_options = [
        { value: 'max_length', label: 'Maximum length' },
        { value: 'starting_with', label: 'Starting with' },
        { value: 'ending_with', label: 'Ending with' },
    ];

    const [selectedOption, setSelectedOption] = useState<OptionInterface|null>(null); 
    const [selectedExtraOption, setSelectedExtraOption] = useState<OptionInterface | null>(null); 
    const [selectedEnabled, setSelectedEnabled] = useState<boolean>(false); 
    const [error, setError] = useState<boolean>(false); 
    const [typeIsSelected, setTypeIsSelected] = useState<boolean>(false); 
    const [name, setName] = useState<string>("custom_data_type"); 
    const [description, setDescription] = useState<string>("new_data_type"); 
    const [extraValue, setExtraValue] = useState<string>(''); 
    const [options, setOptions] = useState<Array<OptionInterface>>([]); 
    const [extraOptions, setExtraOptions] = useState<Array<OptionInterface>>(extra_options); 
    const [extraValidations, setExtraValidations] = useState<Array<ExtraValidationInterface>>([]); 
    

    useEffect(()=>{
        const aux_arr: Array<OptionInterface> = []
        default_data_types.forEach(e=>{
            aux_arr.push({ value: e.data_type, label: e.data_type.charAt(0).toUpperCase() + e.data_type.slice(1)  });
        })
        setOptions(aux_arr)
        setSelectedEnabled(true)
    },[])


    const changeName = (e)=>{
        setName(e.target.value)
    }

    const changeDescription = (e)=>{
        setDescription(e.target.value)
    }

    const changeExtraValue = (e)=>{
        setExtraValue(e.target.value)
    }

    const changeExtraValueNum = (e)=>{
        if (e.target.validity.valid){
            setExtraValue(e.target.value)
        }
    }

    

    const removeCondition = (e)=>{
        console.log("remove condition")
        console.log(e)
        let extra_options_exists = false;
        extraOptions.forEach(el=>{
            if (el.label === e.type){
                extra_options_exists = true
            }
        })
        if (!extra_options_exists){
            setExtraOptions([...extraOptions,{label: e.type,value:extraValue}])
        }

        setExtraValidations(extraValidations.filter(elem=>{
            if (elem.type !== e.type){
                return elem;
            }
        }))
    }

    const addExtraValidation = ()=>{
        if (selectedExtraOption){
            const new_validations = [...extraValidations,{type: selectedExtraOption.label,value:extraValue}]
            setExtraValidations(new_validations)
            setExtraOptions(extraOptions.filter(elem=>{
                if (selectedExtraOption && elem.value !== selectedExtraOption.value){
                    return elem;
                }
            }))
            setSelectedExtraOption(null)
            setExtraValue('')
        }
    }


    const create_new_data_type = () =>{
        let data_type_exists = false;
        if (!selectedOption){
            return
        }
        dataTypes.forEach(element => {
            if (element.data_type === name){
                data_type_exists = true
            }
        });

        if (!data_type_exists){
            const updated_data_types = [...dataTypes,{
                data_type: name, 
                description: description, 
                extra:extraValidations.length > 0 ? extraValidations : null,
                basic_data_type: selectedOption?.value
            }];
            setDataTypes(updated_data_types);
            closeModal()
        }
        else{
            setError(true)
        }
    }


    return(
        <div>
            <h2>Create custom data_types</h2>
            <button id="close_button" onClick={closeModal}>Close modal</button>
            <div>Data_type name</div>
            
            <input type="text" name="data_type_name" onChange={changeName} value={name}/>

            <div>Data_type description</div>
            
            <input type="text" name="data_type_description" onChange={changeDescription} value={description}/>

            <div>Basic datatype</div>
            <Select
                value={selectedOption}
                onChange={(e:OptionInterface|null)=>{
                    console.log(e)
                    if (e!== undefined && e !==null){
                        setTypeIsSelected(true)
                        setSelectedOption(e)}}
                    }
                options={options}
                isDisabled={!selectedEnabled}
            />

            {selectedOption !== null ?
                <div>
                    <div>Extra Validations: customize your validations</div>
                    <div>
                        {extraValidations.length > 0 ?
                            <div style={{display:"flex", flexDirection:"row"}}>
                                <div className="cell">Condition</div>
                                <div className="cell">Condition value</div>
                            </div>
                            :
                            <></>
                        }
                        {extraValidations.map(e=>{
                            console.log(e)
                            return <div style={{display:"flex", flexDirection:"row"}}>
                                    <div className="cell">{e.type}</div>
                                    <div className="cell">{e.value}</div>
                                    <button onClick={()=>removeCondition(e)}>Remove conditon</button>
                                </div>
                        })}
                    </div>
                    <div style={{display:"flex", flexDirection:"row"}}>
                        <Select
                            value={selectedExtraOption}
                            onChange={(e:OptionInterface|null)=>{
                                if (e!== undefined && e !==null){
                                    setSelectedExtraOption(e)}}
                                }
                            options={extraOptions}
                        />
                        {selectedExtraOption !== null ?
                            <>
                                {console.log(selectedExtraOption)}
                                {selectedExtraOption.value === "max_length" ?
                                    <input type="text" name="extra" pattern="[0-9]*" onChange={changeExtraValueNum} value={extraValue}/>
                                    
                                    :
                                    <input type="text" name="extra" onChange={changeExtraValue} value={extraValue}/>
                                }
                            </>
                            :
                            <></>
                            }
                        {selectedExtraOption!==null && extraValue!==''?
                            <button onClick={addExtraValidation}>Add extra validation</button>    
                            :
                            <div>Please select a condition and a value</div>

                        }
                        {/* <button onClick={addExtraValidation} disabled={}>Add extra validation</button> */}
                    </div>
                </div>
                :
                <></>
            }
            

            <button onClick={create_new_data_type} disabled={!typeIsSelected} title={!typeIsSelected ? "Select a basic data_type to enable" : undefined}>Create data_type: "{name}"</button>
            {error ?
                <div>There is an error saving your new data_type. Maybe you are using an already existing data_type name?</div>
                :
                <></>
            }
        </div>
    )
}

export default AddTypeModal;