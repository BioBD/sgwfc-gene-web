import React from 'react'
import Header from '../../components/Header'
import FileUpload from '../FileUpload'
import './index.less'

class App extends React.Component {
  render () {
    const text = 'Django + React Teste';
    return (
      <div className="app--wrapper">
        <Header title={text} />
        <FileUpload />
      </div>
    )
  }
}
export default App