function formateaNumeroChileno(n) {
    if (n == null || "undefined" == typeof(n) || ("string" == typeof(n) && n.length == 0)) {
        return n;
    }
    // Eliminar parte decimal del número
    n = String(n).split(".")[0].replace(/\D/g, "");
    if (n < 0) {
        return "-" + formateaNumeroChileno(Math.abs(n));
    }
    // Agregar separador de miles
    return n.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function procesaNumeroChileno(n) {
    return String(n).replace(/\D/g, "")
}
function formateaKeyUp(event) {
    const target = event.target;
    const value = target.value.replace(/\D/g, "")
    target.value = formateaNumeroChileno(value);
}

document.addEventListener('DOMContentLoaded', (event) => {
    const elementos = document.querySelectorAll('.cambiarNumero');
    elementos.forEach(elemento => {
        if (elemento.tagName === 'INPUT') {
            elemento.value = formateaNumeroChileno(procesaNumeroChileno(elemento.value));
            elemento.addEventListener('input', formateaKeyUp);
        } else if (elemento.tagName === 'TD') {
            elemento.textContent = formateaNumeroChileno(procesaNumeroChileno(elemento.textContent));
        }
    });
});