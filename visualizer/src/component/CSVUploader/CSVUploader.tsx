import React from "react";
import { useCSVReader } from "react-papaparse";
import { ParseResult } from "papaparse";
import { StateData } from "../../types/StateData";
import { styles } from "./style";
import { useCSVConverter } from "../../hooks/useCSVConverter";

interface Props {
  setData: (data: StateData[]) => void;
  setStep: (step: number) => void;
}

export const CSVReader: React.FC<Props> = ({ setData, setStep }) => {
  const { CSVReader } = useCSVReader();
  const { convertResultToState } = useCSVConverter();

  const removeFile = () => {
    setData([]);
    setStep(1);
  };

  return (
    <CSVReader
      onUploadAccepted={(results: ParseResult<string[]>) => {
        setStep(1);
        setData(convertResultToState(results));
      }}
    >
      {({
        getRootProps,
        acceptedFile,
        ProgressBar,
        getRemoveFileProps,
      }: any) => (
        <>
          <div style={styles.csvReader}>
            <button type="button" {...getRootProps()} style={styles.browseFile}>
              Select CSV
            </button>
            <div style={styles.acceptedFile}>
              {acceptedFile && acceptedFile.name}
            </div>
            <button
              {...getRemoveFileProps({ onClick: removeFile })}
              style={styles.remove}
            >
              Remove
            </button>
          </div>
          <ProgressBar style={styles.progressBar} />
        </>
      )}
    </CSVReader>
  );
};
