import React from 'react'
import Button from '../../components/Button'
import './index.less'

class FileUpload extends React.Component {

  async workflow (requestData) {
    const requestOptions = {
      method: 'POST',
      body: JSON.stringify(requestData),
      headers: new Headers({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }),
    }
  
    const response = await fetch('http://localhost:8000/api/workflow/', requestOptions)
    console.log(response.json())
  }

  render () {
    return (
      <div className="file_upload--wrapper">
        <Button text="Upload" height="10%" width="20%" onClickFunction={() => this.workflow({name: "input/STRING/yellow_interactions.csv"})} color="grey" />
      </div>
    )
  }
}
export default FileUpload