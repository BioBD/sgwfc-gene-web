import React, { useState, useEffect } from 'react'
import './index.less'
import CytoscapeComponent from 'react-cytoscapejs'
import Util from '../../util'
import Cytoscape from 'cytoscape';
import fcose from 'cytoscape-fcose';
import {useSelector} from 'react-redux' 
import Loader from "react-loader-spinner";

Cytoscape.use(fcose);

const Graph = () => {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(true);
  const [runFinished, setRunFinished] = useState(false);
  const [items, setItems] = useState([]);
  const [r, setr] = useState([]);
  
  const tokenFile = useSelector((state) => state.tokenFile);
  
  useEffect(() => {    
    if(tokenFile)
    {
      setRunFinished(false);
      setIsLoaded(false);

      const requestData = {tokenFile: tokenFile};
      const csrftoken = Util.getCookie('csrftoken');
      
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
          const r = {};
          
          r['edges']= result['edges'].splice(0,500);
          r['nodes'] = result['nodes'].splice(0, 501);
          
          setr(r);              
          setRunFinished(true);
          setIsLoaded(true);
        },
        (error) => {
          setRunFinished(true);
          setIsLoaded(true);
          setError(error);
        }
      )
    }
  },[tokenFile])

    const layout =  {
      name: 'fcose',

      // 'draft', 'default' or 'proof'
      // - "draft" only applies spectral layout 
      // - "default" improves the quality with incremental layout (fast cooling rate)
      // - "proof" improves the quality with incremental layout (slow cooling rate) 
      quality: "proof",
      // Use random node positions at beginning of layout
      // if this is set to false, then quality option must be "proof"
      randomize: true,
      // Whether or not to animate the layout
      animate: false,
      // Duration of animation in ms, if enabled
      animationDuration: 1000,
      // Easing of animation, if enabled
      animationEasing: undefined,
      // Fit the viewport to the repositioned nodes
      fit: true,
      // Padding around layout
      padding: 30,
      // Whether to include labels in node dimensions. Valid in "proof" quality
      nodeDimensionsIncludeLabels: false,
      // Whether or not simple nodes (non-compound nodes) are of uniform dimensions
      uniformNodeDimensions: true,
      // Whether to pack disconnected components - cytoscape-layout-utilities extension should be registered and initialized
      packComponents: false,
      // Layout step - all, transformed, enforced, cose - for debug purpose only
      step: "all",
      
      /* spectral layout options */
      
      // False for random, true for greedy sampling
      samplingType: true,
      // Sample size to construct distance matrix
      sampleSize: 500,
      // Separation amount between nodes
      nodeSeparation: 1000,
      // Power iteration tolerance
      piTol: 0.0000001,
      
      /* incremental layout options */
      
      // Node repulsion (non overlapping) multiplier
      nodeRepulsion: node => 1500000,
      // Ideal edge (non nested) length
      idealEdgeLength: edge => 50,
      // Divisor to compute edge forces
      edgeElasticity: edge => 0.05,
      // Nesting factor (multiplier) to compute ideal edge length for nested edges
      nestingFactor: 0.1,
      // Maximum number of iterations to perform - this is a suggested value and might be adjusted by the algorithm as required
      numIter: 2500,
      // For enabling tiling
      tile: true,
      // Represents the amount of the vertical space to put between the zero degree members during the tiling operation(can also be a function)
      tilingPaddingVertical: 10,
      // Represents the amount of the horizontal space to put between the zero degree members during the tiling operation(can also be a function)
      tilingPaddingHorizontal: 10,
      // Gravity force (constant)
      gravity: 0.25,
      // Gravity range (constant) for compounds
      gravityRangeCompound: 1.5,
      // Gravity force (constant) for compounds
      gravityCompound: 1.0,
      // Gravity range (constant)
      gravityRange: 3.8,
      // Initial cooling factor for incremental layout
      initialEnergyOnIncremental: 0.3,

      /* constraint options */

      // Fix desired nodes to predefined positions
      // [{nodeId: 'n1', position: {x: 100, y: 200}}, {...}]
      fixedNodeConstraint: undefined,
      // Align desired nodes in vertical/horizontal direction
      // {vertical: [['n1', 'n2'], [...]], horizontal: [['n2', 'n4'], [...]]}
      alignmentConstraint: undefined,
      // Place two nodes relatively in vertical/horizontal direction
      // [{top: 'n1', bottom: 'n2', gap: 100}, {left: 'n3', right: 'n4', gap: 75}, {...}]
      relativePlacementConstraint: undefined,

      /* layout event callbacks */
      ready: () => {}, // on layoutready
      stop: () => {} // on layoutstop
  };

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
  const style =  { background: 'white', width: '90%', height: '800px', border:'2px solid #808080', borderRadius:'5px' };

  const elements = [
    { data: { id: 'one', label: 'Node 1' }},
    { data: { id: 'two', label: 'Node 2' }},
    { data: { source: 'one', target: 'two', label: 'Edge from Node1 to Node2' } }
  ];
      
  const runWorkflow = (tokenFile) => {    
   
  }

  /*
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
          const r = {};
          
          r['edges']= result['edges'].splice(0,500);
          r['nodes'] = result['nodes'].splice(0, 501);
          
          setr(r);        
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [])
  //*/
  //  <CytoscapeComponent elements={elements} zoom={1}  style={style} layout={layout} />  
  if (runFinished) {
    return (
      <div className="graph--wrapper">
        <CytoscapeComponent elements={CytoscapeComponent.normalizeElements(r)} minZoom={0.2} zoom={0.8} maxZoom={1.5} layout={layout} stylesheet={stylesheet} style={style} />                              
      </div>
    )
  }
  else {
    if(isLoaded)
    {
      return <div> </div>;
    }
    else {
      return <Loader type="Puff" color="#00BFFF" height={100} width={100} />; //3 secs/>
    }    
  }
}
export default Graph
