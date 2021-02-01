import React, { useState, useEffect } from 'react'
import './index.less'
import CytoscapeComponent from 'react-cytoscapejs'

const Graph = () => {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const layout = { name: 'grid' }
  const stylesheet = [{
      selector: "node",
      css: {
        label: "data(id)", 
        shape: "rectangle"
      }
    },
    {
      selector: "edge",
      css: {
        "curve-style": "bezier",
        "control-point-step-size": 40,
        "target-arrow-shape": "triangle"
      }
    }
  ]
  const style = { width: '800px', height: '800px' }

  useEffect(() => {
    const requestData = {name: "input/STRING/yellow_interactions.csv"};
    const requestOptions = {
      method: 'POST',
      body: JSON.stringify(requestData),
      headers: new Headers({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }),
    }
  
    fetch('/api/workflow/', requestOptions)
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setItems(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [])

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return (
      <CytoscapeComponent elements={CytoscapeComponent.normalizeElements(items)} zoom={0.5} layout={layout} stylesheet={stylesheet} style={style} />
    )
  }

}
export default Graph
