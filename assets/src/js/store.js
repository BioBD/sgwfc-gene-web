import {createStore} from 'redux'

//poderia estruturar os dados que minha aplicacao poderia usar
const INITIAL_STATE = {
    tokenFile: '',
    loading: false
}

/*
action é um objeto vai ter dois parametros:
- tipo/nome de ação que eu quero (play, pause e etc)
- valor
*/
const reducer = (state = INITIAL_STATE, action) => { //es6 arrow function
    
    switch (action.type) {
       case 'RUN':
            return {...state, tokenFile:action.value }
       case 'LOADING':
                return {...state, loading:action.value }
       default:
          return state;
    }
}

const store = createStore(reducer)

export default store