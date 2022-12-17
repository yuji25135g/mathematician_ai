import React, { useState } from "react";
import {
  useCSVReader,
  lightenDarkenColor,
  formatFileSize,
} from "react-papaparse";
import { styles } from "./style";

interface Props {
  setData: React.SetStateAction<any>;
}

export const CSVReader: React.FC<Props> = ({ setData }) => {
  const { CSVReader } = useCSVReader();
  const [zoneHover, setZoneHover] = useState(false);
  const [removeHoverColor, setRemoveHoverColor] = useState("#A01919");

  return (
    <CSVReader
      onUploadAccepted={(results: any) => {
        console.log("---------------------------");
        console.log(results);
        const data = results.data
          .filter((d: any) => d.length === 3)
          .map((d: any) => ({
            from: d[0],
            probs: d[1].split(","),
            nodes: d[2].split("_"),
          }));
        setData(data);
        console.log("---------------------------");
        setZoneHover(false);
      }}
      onDragOver={(event: DragEvent) => {
        event.preventDefault();
        setZoneHover(true);
      }}
      onDragLeave={(event: DragEvent) => {
        event.preventDefault();
        setZoneHover(false);
      }}
    >
      {({
        getRootProps,
        acceptedFile,
        ProgressBar,
        getRemoveFileProps,
        Remove,
      }: any) => (
        <>
          <div
            {...getRootProps()}
            style={Object.assign(
              {},
              styles.zone,
              zoneHover && styles.zoneHover
            )}
          >
            {acceptedFile ? (
              <>
                <div style={styles.file}>
                  <div style={styles.info}>
                    <span style={styles.size}>
                      {formatFileSize(acceptedFile.size)}
                    </span>
                    <span style={styles.name}>{acceptedFile.name}</span>
                  </div>
                  <div style={styles.progressBar}>
                    <ProgressBar />
                  </div>
                  <div
                    {...getRemoveFileProps()}
                    style={styles.remove}
                    onMouseOver={(event: Event) => {
                      event.preventDefault();
                      setRemoveHoverColor(lightenDarkenColor("#A01919", 40));
                    }}
                    onMouseOut={(event: Event) => {
                      event.preventDefault();
                      setRemoveHoverColor("#A01919");
                    }}
                  >
                    <Remove color={removeHoverColor} />
                  </div>
                </div>
              </>
            ) : (
              "Drop CSV file here or click to upload"
            )}
          </div>
        </>
      )}
    </CSVReader>
  );
};
