import React from 'react'
import Header from '../../components/Header'

class App extends React.Component {
  render () {
    const text = 'Django + React Teste';
    return (
      <Header title={text} />
    )
  }
}
export default App