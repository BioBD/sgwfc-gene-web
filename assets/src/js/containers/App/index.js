import React from 'react'
import {Provider} from 'react-redux'
import store from '../../store'
import Header from '../../components/Header'
import FileUpload from '../FileUpload'
import Graph from '../../components/Graph'
import FilesUser from '../../components/FilesUser'
import './index.less'

class App extends React.Component {

  render () {
    const text = '';

    return (
      <div className="app--wrapper">
       <Provider store={store}>
          <Header title={text} />
          <FileUpload />
          <FilesUser />
          <Graph />
       </Provider>
      </div>
    )
  }
}
export default App