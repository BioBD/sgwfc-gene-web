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

    //alert(id);
    //passar id para uma funcao do componente do cytoscape. Lá ele vai receber o id fazer uma request para o back e pegar o arquivo e rodar o workflow e mostrar o resultado na tela
  }

  const deleteFile= (event) => {
     var id = $(event.target).closest('tr').attr('data-key');
     alert(id);

     const requestOptions = {
      method: 'GET',
      headers: new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      })
    }
    /*fetch('/api/deleteFileUser?id='+id, requestOptions)
      .then(res => res.json())
      .then(
        (result) => {
          if(result.error)
          {
            alert('Erro ao deleter arquivo!');
          }
          else 
          {
            //apagar elemento da tabela!
          }
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )     */
  }
  /*
  const data = React.useMemo(
    () => [
      {
        col1: 'Hello',
        col2: 'World',
      },
      {
        col1: 'react-table',
        col2: 'rocks',
      },
      {
        col1: 'whatever',
        col2: 'you want',
      },
    ],
    []
  )

  const columns = React.useMemo(
    () => [
      {
        Header: 'Name',
        accessor: 'col1', // accessor is the "key" in the data
      },
      {
        Header: '	Upload date',
        accessor: 'col2',
      },
      {
        Header: '',
        accessor: 'col2',
      }
    ],
    []
  )
  
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data })
  */

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

  //<CytoscapeComponent elements={CytoscapeComponent.normalizeElements(r)} minZoom={0.2} zoom={0.8} maxZoom={1.5} layout={layout} stylesheet={stylesheet} style={style} />                  
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
          </tr>
        </thead>
        <tbody>
          { 
           files.map(item => (
            <tr data-key={item.id}>
              <td>{item.name}</td>
              <td>{item.date_upload}</td>
              <td><a href="#" onClick={runWorkflow}>Run</a></td>
              <td><a href="#" onClick={deleteFile}>Delete</a></td>              
            </tr>
          ))}
        </tbody>
      </table>
      </div>
    )
  }
}
export default FilesUser
