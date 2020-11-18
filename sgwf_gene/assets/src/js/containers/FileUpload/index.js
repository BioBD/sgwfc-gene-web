import React from 'react'
import Button from '../../components/Button'
import './index.less'

class FileUpload extends React.Component {

  onButtonClick () {
    console.log("Hello")
  }

  render () {
    return (
      <div className="file_upload--wrapper">
        <Button text="Upload" height="10%" width="20%" onClickFunction={this.onButtonClick} color="grey" />
      </div>
    )
  }
}
export default FileUpload