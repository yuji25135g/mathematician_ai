import { CSSProperties } from "react";

export const styles = {
  csvReader: {
    display: "flex",
    flexDirection: "row",
  } as CSSProperties,
  browseFile: {
    width: "20%",
  } as CSSProperties,
  acceptedFile: {
    border: "1px solid #ccc",
    height: 45,
    paddingLeft: 10,
    width: "80%",
  } as CSSProperties,
  remove: {
    borderRadius: 0,
    padding: "0 20px",
  } as CSSProperties,
  progressBar: {
    backgroundColor: "#87cefa",
    height: 5,
  } as CSSProperties,
};
