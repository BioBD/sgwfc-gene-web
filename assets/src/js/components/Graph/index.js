import React, { useState, useEffect } from 'react'
import './index.less'
import CytoscapeComponent from 'react-cytoscapejs'
import Util from '../../util'

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
  const style =  { background: 'white', width: '90%', height: '950px', border:'2px solid #808080', borderRadius:'5px' }

  const csrftoken = Util.getCookie('csrftoken');

  const elements = [
    { data: { id: 'one', label: 'Node 1' }, position: { x: 100, y: 100 } },
    { data: { id: 'two', label: 'Node 2' }, position: { x: 200, y: 300 } },
    { data: { source: 'one', target: 'two', label: 'Edge from Node1 to Node2' } }
  ];

  useEffect(() => {
    const requestData = {name: "input/STRING/yellow_interactions.csv"};
    const requestOptions = {
      method: 'POST',
      body: JSON.stringify(requestData),
      headers: new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      })
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
//
//<CytoscapeComponent elements={elements}  style={ } />          

  return (
    <div className="graph--wrapper">
      <CytoscapeComponent elements={CytoscapeComponent.normalizeElements(items)} minZoom={0.8} zoom={1.5} maxZoom={2.5} layout={layout} stylesheet={stylesheet} style={style} />              
    </div>
  )
  

}
export default Graph
