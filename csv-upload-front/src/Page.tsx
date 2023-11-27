import './App.css';
import React from "react";
import FileUpload from './Components/FileUpload.tsx'
import Intro from './Components/Intro.tsx'
import DataTypeTable from './Components/DataTypeTable.tsx';
import AddTypeModal from './Components/AddTypeModal.tsx';

interface ExtraValidationInterface {
  type: string,
  value: string
}

interface DataTypeInterface {
  data_type: string,
  description: string,
  extra?: [ExtraValidationInterface],
  basic_data_type?: string
}

const default_data_types:Array<DataTypeInterface> = [
  {data_type:"decimal", description:"Checks if it is a decimal number"},
  {data_type:"integer", description:"Checks if it is an integer number"},
  {data_type:"string", description:"Checks if it is a string"},
  {data_type:"url", description:"Checks if it is a valid url"}
];


const Page = () => {
  const [dataTypes, setDataTypes] = React.useState(default_data_types);
  const [modalIsOpen, setIsOpen] = React.useState(false);

  const closeModal = () => {
    setIsOpen(false);
  }

  const openModal = () => {
    setIsOpen(true);
  }


  return (
    <div className="App">
      <div className="App-header" style={{padding: "10px"}}>
        <Intro/>
        <DataTypeTable dataTypes={dataTypes} openModal={openModal}/>
        <FileUpload dataTypes={dataTypes} />
        <AddTypeModal default_data_types={default_data_types} dataTypes={dataTypes} setDataTypes={setDataTypes} closeModal={closeModal} modalIsOpen={modalIsOpen} />
      </div>
    </div>
  );
}

export default Page;
