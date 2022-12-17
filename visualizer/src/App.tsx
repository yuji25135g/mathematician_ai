import React, { useState } from "react";
import "./App.css";
import Typography from "@mui/material/Typography";
import Pagination from "@mui/material/Pagination";
import { CSVReader } from "./CSVUploader/CSVUploader";
import { StateNetwork } from "./StateNetwork/StateNetwork";

const App = () => {
  const [step, setStep] = useState(1);
  const [data, setData] = useState<any[]>([]);

  const handleChangeStep = (
    event: React.ChangeEvent<unknown>,
    value: number
  ) => {
    setStep(value);
  };

  return (
    <>
      <CSVReader setData={setData} />
      <StateNetwork data={data} step={step} />
      <Typography>Step: {step}</Typography>
      <Pagination count={data.length} page={step} onChange={handleChangeStep} />
    </>
  );
};

export default App;
