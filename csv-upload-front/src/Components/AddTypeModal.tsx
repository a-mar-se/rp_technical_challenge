import React, { useEffect, useState } from "react";
import Select from 'react-select';
import Modal from  'react-modal';
import InputComp from "./Modal/InputComp.tsx";
import NumberInputComp from "./Modal/NumberInputComp.tsx";

interface OptionInterface {
    label: string,
    value: string
}

interface ExtraValidationInterface {
    type: string,
    value: string
}

const AddTypeModal = ({default_data_types, dataTypes, setDataTypes, closeModal, modalIsOpen}) => {
    const extra_options = [
        { value: 'max_length', label: 'Maximum length' },
        { value: 'starting_with', label: 'Starting with' },
        { value: 'contains', label: 'Contains characters' },
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
    const [nDecimals, setNDecimals] = useState<number>(0); 
    const [decimalPoint, setDecimalPoint] = useState<string>('.'); 
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


    

    const removeExtraValidation = (e)=>{
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


    const createNewDataType = () =>{
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
            
            if (selectedOption.value !== "decimal"){
                const updated_data_types = [...dataTypes,{
                    data_type: name, 
                    description: description, 
                    extra:extraValidations.length > 0 ? extraValidations : null,
                    basic_data_type: selectedOption?.value
                }];
                setDataTypes(updated_data_types);
            }
            else{
                const aux_extra_validations = [...extraValidations,{type: "decimal_point",value:decimalPoint}]
                if (nDecimals !== 0){
                    aux_extra_validations.push({type: "n_decimals",value:""+nDecimals})
                }
                const updated_data_types = [...dataTypes,{
                    data_type: name, 
                    description: description, 
                    extra: aux_extra_validations,
                    basic_data_type: selectedOption?.value
                }];
                setDataTypes(updated_data_types);
                
            }
            closeModal()
        }
        else{
            setError(true)
        }
    }


    return(
        <Modal
                isOpen={modalIsOpen}
                onRequestClose={closeModal}
            >
            <div style={{}}>
                <h2>Create custom data_types</h2>
                <button id="close_button" onClick={closeModal}>Close modal</button>
                
                <div className="section row">
                    <div>Data_type name</div>
                    <InputComp changeInput={setName} inputValue={name} />
                </div>

                <div className="section row">
                    <div>Data_type description</div>
                    <InputComp changeInput={setDescription} inputValue={description} />
                </div>

                {/* Simple data_type selection: integer, decimal, string or url */}
                <div className="section row">
                    <div>Basic datatype</div>
                    <Select
                        value={selectedOption}
                        onChange={(e:OptionInterface|null)=>{
                            if (e!== undefined && e !==null){
                                setTypeIsSelected(true)
                                setSelectedOption(e)}}
                            }
                        options={options}
                        isDisabled={!selectedEnabled}
                    />
                </div>

                {/* Once you select your basic data_type, there will appear some components to allow to customize the validation */}
                {selectedOption !== null ?
                    <div className="section">
                        <h5>Extra Validations: customize your validations</h5>
                        {/* This is a table showing your custom conditions for validation */}
                        <div>
                            {/* Table headers */}
                            <div style={{display:"flex", flexDirection:"row"}}>
                                <div className="cell dark-border">Condition</div>
                                <div className="cell dark-border">Condition value</div>
                            </div>

                            {/* Your already defined custom conditions to your custom data_type  */}
                            {extraValidations.map(e=>{
                                return <div style={{display:"flex", flexDirection:"row"}}>
                                        <div className="cell dark-border">{e.type}</div>
                                        <div className="cell dark-border">{e.value}</div>
                                        <button onClick={()=>removeExtraValidation(e)}>Remove conditon</button>
                                    </div>
                            })}
                            
                            {selectedOption.label === "Decimal" ?
                                <div style={{display: "flex", flexDirection:'row'}}>
                                    <div className="cell dark-border">Decimal point</div>
                                    <div className="cell dark-border" >
                                        <div className="row">
                                            <label>
                                                <input type="checkbox" checked={decimalPoint === '.'}
                                                    onChange={() => setDecimalPoint('.')}
                                                    />
                                                <span>.</span>
                                            </label>
                                        </div>
                                        <div className="row">
                                            <label>
                                                <input type="checkbox" checked={decimalPoint === ','}
                                                    onChange={() => setDecimalPoint(',')}
                                                    />
                                                <span>,</span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                :
                                <></>
                            }


                            {selectedOption.label === "Decimal" ?
                                <div style={{display: "flex", flexDirection:'row'}}>
                                    <div className="cell dark-border">Number of decimals</div>
                                    <div className="cell dark-border" >
                                        <div className="row">
                                            <label>
                                                <NumberInputComp changeInput={setNDecimals} inputValue={nDecimals}/>
                                            </label>
                                        </div>
                                    </div>

                                    <div className="cell dark-border" >
                                        <div>(0 for any number of decimals)</div>
                                    </div>
                                </div>
                                :
                                <></>
                            }

                            {/* Adding conditions to your custom data_type  */}
                            <div style={{display:"flex", flexDirection:"row"}}>
                                {/* Select extra conditions for validation of your custom data_type */}
                                <div className="cell dark-border">
                                    <Select
                                        value={selectedExtraOption}
                                        onChange={(e:OptionInterface|null)=>{
                                            if (e!== undefined && e !==null){
                                                setSelectedExtraOption(e)}}
                                            }
                                        options={extraOptions}
                                    />
                                </div>

                                {/* If an extra condition is selected, there will appear a textbox to include the condition value. */}
                                {selectedExtraOption !== null ?
                                    <div className="cell dark-border">
                                        {selectedExtraOption.value === "max_length" ?
                                            <NumberInputComp changeInput={setExtraValue} inputValue={extraValue} />
                                            :
                                            <InputComp changeInput={setExtraValue} inputValue={extraValue} />
                                        }
                                    </div>
                                    :
                                    <></>
                                }
                                {/* If an extra condition is selected and a value different from "" assigned, a button will appear to store the new condition. */}
                                {selectedExtraOption!==null && extraValue!==''?
                                    <button onClick={addExtraValidation}>Add extra validation</button>    
                                    :
                                    <div>Select a condition and a value</div>

                                }
                            </div>
                        </div>

                    </div>
                    :
                    <></>
                }
                
                {/* This is the button to store the newly created data_type. Clicking it will close the modal and inmediately show all default data_types with your custom ones. */}
                <button onClick={createNewDataType} disabled={!typeIsSelected} title={!typeIsSelected ? "Select a basic data_type to enable" : undefined}>Create data_type: "{name}"</button>
                
                {/* Error message when there are problems storing the custom data_type */}
                {error ?
                    <div>There is an error saving your new data_type. Maybe you are using an already existing data_type name?</div>
                    :
                    <></>
                }
            </div>
        </Modal>
    )
}

export default AddTypeModal;