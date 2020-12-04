import React from 'react'
import './index.less'
import CytoscapeComponent from 'react-cytoscapejs'

const Graph = ({  }) => {
  const elements = [
    { data: { id: 'one', label: 'Node 1' }, position: { x: 0, y: 0 } },
    { data: { id: 'two', label: 'Node 2' }, position: { x: 100, y: 0 } },
    { data: { source: 'one', target: 'two', label: 'Edge from Node1 to Node2' } }
  ]
  const layout = { name: 'random' }

  return (
    <CytoscapeComponent elements={elements} layout={layout} style={ { width: '600px', height: '600px' } } />
  )
}
export default Graph