document.getElementById('div_id_placaPatente').classList.add('col-md-4');
document.getElementById('div_id_rutPropietario').classList.add('col-md-4');
document.getElementById('div_id_tenencia').classList.add('col-md-4');
document.getElementById('div_id_nombrePropietario').classList.add('col-md-4');
document.getElementById('div_id_domicilio').classList.add('col-md-4');
document.getElementById('div_id_tipo').classList.add('col-md-4');
document.getElementById('div_id_ano').classList.add('col-md-4');
document.getElementById('div_id_marca').classList.add('col-md-4');
document.getElementById('div_id_modelo').classList.add('col-md-4');
document.getElementById('div_id_numeroMotor').classList.add('col-md-4');
document.getElementById('div_id_numeroChasis').classList.add('col-md-4');
document.getElementById('div_id_numeroVin').classList.add('col-md-4');
document.getElementById('div_id_color').classList.add('col-md-4');
document.getElementById('div_id_fechaVencimientoPermisoCirculacion').classList.add('col-md-4');
document.getElementById('div_id_fechaVencimientoRevisionTecnica').classList.add('col-md-4');
document.getElementById('div_id_fechaVencimientoSeguroObligatorio').classList.add('col-md-4');

const inputs = document.querySelectorAll('input');
const selects = document.querySelectorAll('select');
inputs.forEach(ctrl => {
    ctrl.dataset.value = ctrl.value;
    ctrl.addEventListener('input', e => {
        if ( ctrl.value != ctrl.dataset.value) {
            ctrl.classList.add('changed');
        }else{
            ctrl.classList.remove('changed');
        }
    });
});

selects.forEach(ctrl => {
    ctrl.dataset.value = ctrl.value;
    ctrl.addEventListener('change', e => {
        if ( ctrl.value != ctrl.dataset.value) {
            ctrl.classList.add('changed');
        }else{
            ctrl.classList.remove('changed');
        }
    });
});
form.onsubmit = e => {
    window.onbeforeunload = e => { return null };
}
window.onbeforeunload = e => {
    const mustConfirm = document.querySelectorAll('.changed').length > 0;
    return mustConfirm ? ' ' : null;
}

function formatRutPropietario(id_rutPropietario)
    {id_rutPropietario.value=id_rutPropietario.value.replace(/[.-]/g, '')
    .replace( /^(\d{1,2})(\d{3})(\d{3})(\w{1})$/, '$1.$2.$3-$4')}
