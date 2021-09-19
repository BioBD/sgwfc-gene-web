import React, { useState, useEffect }from 'react'
import Button from '../../components/Button'
import './index.less'
import Util from '../../util'

const FileUpload = () => {

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(true);

    const csrftoken = Util.getCookie('csrftoken');

    const fileUploadHandler = event => {
    
      const file = event.target.files[0];
      const formaData = new FormData();
      formaData.append('csv', file);
            
      const requestOptions = {
        method: 'POST',
        body: formaData,
        headers: { "X-CSRFToken": csrftoken }
      }

      setIsLoaded(false);    
      fetch('/api/uploadFile/', requestOptions)
        .then(res => res.json()) 
        .then(
          (result) => {
            setIsLoaded(true);
            if(!result.error)
            {
              alert('csv file saved successfully');
            }
            else
            {
              alert(result.message);
            }
          },
          (error) => {
            setIsLoaded(true);
            setError(error);
          }
        )
    }

    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      //<Button text="Upload" height="10%" width="20%" color="grey" />
      return (
        <div className="file_upload--wrapper">
        <input type="file" onChange={fileUploadHandler} />
        </div>
      )
    }
} 

export default FileUpload 