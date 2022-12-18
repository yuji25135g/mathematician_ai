import React, { useState } from "react";
import "./App.css";
import Typography from "@mui/material/Typography";
import Pagination from "@mui/material/Pagination";
import { CSVReader } from "./component/CSVUploader/CSVUploader";
import { StateNetwork } from "./component/StateNetwork/StateNetwork";
import { StateData } from "./types/StateData";

const App = () => {
  const [step, setStep] = useState(1);
  const [data, setData] = useState<StateData[]>([]);

  const handleChangeStep = (
    event: React.ChangeEvent<unknown>,
    value: number
  ) => {
    setStep(value);
  };

  return (
    <>
      <CSVReader setData={setData} setStep={setStep} />
      <StateNetwork data={data} step={step} />
      <Typography>Step: {step}</Typography>
      <Pagination count={data.length} page={step} onChange={handleChangeStep} />
    </>
  );
};

export default App;
