import { CSSProperties } from "react";

export const styles = {
  zone: {
    alignItems: "center",
    border: `2px dashed #CCC`,
    borderRadius: 20,
    display: "flex",
    flexDirection: "column",
    height: "10%",
    justifyContent: "center",
    padding: 20,
  } as CSSProperties,
  file: {
    background: "linear-gradient(to bottom, #EEE, #DDD)",
    borderRadius: 20,
    display: "flex",
    height: 120,
    width: 120,
    position: "relative",
    zIndex: 10,
    flexDirection: "column",
    justifyContent: "center",
  } as CSSProperties,
  info: {
    alignItems: "center",
    display: "flex",
    flexDirection: "column",
    paddingLeft: 10,
    paddingRight: 10,
  } as CSSProperties,
  size: {
    backgroundColor: "rgba(255, 255, 255, 0.4)",
    borderRadius: 3,
    marginBottom: "0.5em",
    justifyContent: "center",
    display: "flex",
  } as CSSProperties,
  name: {
    backgroundColor: "rgba(255, 255, 255, 0.4)",
    borderRadius: 3,
    fontSize: 12,
    marginBottom: "0.5em",
  } as CSSProperties,
  progressBar: {
    bottom: 14,
    position: "absolute",
    width: "100%",
    paddingLeft: 10,
    paddingRight: 10,
  } as CSSProperties,
  zoneHover: {
    borderColor: "#686868",
  } as CSSProperties,
  default: {
    borderColor: "#CCC",
  } as CSSProperties,
  remove: {
    height: 23,
    position: "absolute",
    right: 6,
    top: 6,
    width: 23,
  } as CSSProperties,
};
