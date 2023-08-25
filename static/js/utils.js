function validarRut(rut) {
    if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test(rut)) {
      return false;
    }
    var tmp = rut.split('-');
    var digv = tmp[1];
    var rut = tmp[0];
    if (digv == 'K') {
      digv = 'k';
    }
    return (dv(rut) == digv);
  }
  
  function dv(T) {
    var M = 0, S = 1;
    for (; T; T = Math.floor(T / 10)) {
      S = (S + T % 10 * (9 - M++ % 6)) % 11;
    }
    return S ? S - 1 : 'k';
  }

  function testing(){
    console.log("importado exitosamente");
  }

  function formatNumero(number) {
    return new Intl.NumberFormat("ES-CL").format(number)
}