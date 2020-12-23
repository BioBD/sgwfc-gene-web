import React from 'react'
import Header from '../../components/Header'
import FileUpload from '../FileUpload'
import Graph from '../../components/Graph'
import './index.less'

class App extends React.Component {

  render () {
    const text = 'Django + React Teste';
    return (
      <div className="app--wrapper">
        <Header title={text} />
        <FileUpload />
        <Graph />
      </div>
    )
  }
}
export default App