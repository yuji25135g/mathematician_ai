import React, { useMemo } from "react";
import { v4 } from "uuid";
import Graph from "react-graph-vis";
import { useStateGraphData } from "../../hooks/useStateGraphData";
import { StateData } from "../../types/StateData";

interface Props {
  data: StateData[];
  step: number;
}

export const StateNetwork: React.FC<Props> = ({ data, step }) => {
  const { graph, events } = useStateGraphData(data, step);

  const version = useMemo(v4, [graph, step]);

  const options = {
    layout: {
      hierarchical: true,
    },
    edges: {
      color: "#000000",
    },
    height: "80%",
  };

  return (
    <div style={{ height: "80%" }}>
      <Graph key={version} graph={graph} options={options} events={events} />
    </div>
  );
};
