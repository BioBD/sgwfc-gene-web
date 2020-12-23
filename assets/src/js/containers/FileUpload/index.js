import React from 'react'
import Button from '../../components/Button'
import './index.less'

class FileUpload extends React.Component {


  render () {
    return (
      <div className="file_upload--wrapper">
        <Button text="Upload" height="10%" width="20%" color="grey" />
      </div>
    )
  }
}
export default FileUpload