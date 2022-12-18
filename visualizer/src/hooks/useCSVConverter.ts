import { ParseResult } from "papaparse";
import { StateData } from "../types/StateData";

interface CSVConverter {
  convertResultToState: (result: ParseResult<string[]>) => StateData[];
}

export const useCSVConverter = (): CSVConverter => {
  const convertResultToState = (result: ParseResult<string[]>) => {
    if (result.errors.length > 0) {
      return [];
    }

    const stateData = result.data
      .filter((d) => d.length === 3)
      .map((d) => ({
        from: d[0],
        probs: d[1].split(","),
        nodes: d[2].split("_"),
      }));

    return stateData;
  };

  return { convertResultToState };
};
