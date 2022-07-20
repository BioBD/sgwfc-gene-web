import React, { useState, useEffect } from 'react'
import './index.less'
import Util from '../../util'
import {useDispatch} from 'react-redux'
import { connect } from 'react-redux'
//import { useTable } from 'react-table'

const FilesUser = () => {
  
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [files, setFiles] = useState([]);
  const csrftoken = Util.getCookie('csrftoken');
  const dispatch = useDispatch()

  const runWorkflow = (event) => {
    //$('.filesUser--wrapper').hide();
    var id = $(event.target).closest('tr').attr('data-key');
    dispatch({type:'RUN', value:id})
    console.log(id);
    //alert(id);
    //passar id para uma funcao do componente do cytoscape. Lá ele vai receber o id fazer uma request para o back e pegar o arquivo e rodar o workflow e mostrar o resultado na tela
  }

  const deleteFile = (event) => {
    var table_row = $(event.target).closest('tr');
    var id = table_row.attr('data-key');
    var index = table_row.attr('data-index');
    console.log(id);
    console.log(index)

    const requestOptions = {
      method: 'GET',
      headers: new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      })
    }

    fetch('/api/deleteFileUser?id=' + id, requestOptions)
      .then(res => res.json())
      .then(
        (result) => {
          const rows = [...files]
          rows.splice(index, 1);
          setFiles(rows);
        },
        (error) => {
          setError(error);
        }
      )
  }

  const downloadResult = (event) => {
    var id = $(event.target).closest('tr').attr('data-key');
    alert(id);

    const requestOptions = {
      method: 'GET',
      headers: new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      })
    }
  }

  useEffect(() => {
    const requestOptions = {
      method: 'GET',
      headers: new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      })
    }
    fetch('/api/getFilesUser/', requestOptions)
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setFiles(result.files);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [])

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return (
    
    <div className="filesUser--wrapper">
      <h4>User upload file:</h4>
      <table id="table-file-user" border={1} cellPadding={5}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Upload date</th>
            <th colspan="2">Actions</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          { 
            files.map((item, index) => (
              <tr data-key={item.id} data-index={index}>
                <td>{item.name}</td>
                <td>{item.date_upload}</td>
                <td><a href="#" onClick={runWorkflow}>Run</a></td>
                <td><a href="#" onClick={deleteFile}>Delete</a></td>
                <td><a href="#" onClick={downloadResult}>Download</a></td>
              </tr>
            ))
          }
        </tbody>
      </table>
      </div>
    )
  }
}
export default FilesUser