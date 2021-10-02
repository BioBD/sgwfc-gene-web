const Util  = {

    getCookie:  function(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    verificaExtensao(input, extensoes) {
        
        var extPermitidas = extensoes;
        var extArquivo = input.split('.').pop();
      
        if(typeof extPermitidas.find(function(ext){ return extArquivo == ext; }) == 'undefined') {
          return false;
        } else {
          return true;
        }
      }
    
}
export default Util