import React, { useMemo } from "react";
import { v4 } from "uuid";
import Graph from "react-graph-vis";

interface Props {
  data: any[];
  step: number;
}

export const StateNetwork: React.FC<Props> = ({ data, step }) => {
  const graph = {
    nodes: [
      "A |- A",
      ...new Set(
        data
          .slice(0, step)
          .map((d) => d.nodes)
          .flat()
      ),
    ].map((d) => ({ id: d, label: d })),
    edges: data
      .slice(0, step)
      .filter((d) => d.from)
      .map((d) =>
        d.nodes.map((n: any, i: any) => ({
          from: d.from,
          to: n,
          label: d.probs[i].toString(),
        }))
      )
      .flat()
      .filter(
        (d, i, array) =>
          array.findIndex(
            (e) => e.from === d.from && e.label === d.label && e.to === d.to
          ) === i
      ),
  };

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

  const events = {
    select: function (event: any) {
      let { nodes, edges } = event;
    },
  };

  return (
    <div style={{ height: "80%" }}>
      <Graph key={version} graph={graph} options={options} events={events} />
    </div>
  );
};
