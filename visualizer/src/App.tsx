import React, { useState, useMemo } from "react";
import "./App.css";
import Graph from "react-graph-vis";
import Typography from "@mui/material/Typography";
import Pagination from "@mui/material/Pagination";
import { v4 } from "uuid";

const data = [
  { from: null, probs: [], nodes: ["A |- A"] },
  { from: "A |- A", probs: [0.5], nodes: ["!A |- A"] },
  { from: "!A |- A", probs: [0.2], nodes: ["!A |- !A"] },
];

const App = () => {
  const [step, setStep] = useState(1);

  const handleChangeStep = (
    event: React.ChangeEvent<unknown>,
    value: number
  ) => {
    setStep(value);
  };

  const graph = {
    nodes: [
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
        d.nodes.map((n, i) => ({
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

  console.log(graph.edges);

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
    <>
      <div style={{ height: "80%" }}>
        <Graph key={version} graph={graph} options={options} events={events} />
      </div>
      <Typography>Step: {step}</Typography>
      <Pagination count={data.length} page={step} onChange={handleChangeStep} />
    </>
  );
};

export default App;
