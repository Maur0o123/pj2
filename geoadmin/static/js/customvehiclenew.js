const addClass = (id, cls) => { const el = document.getElementById(id); if (el) el.classList.add(cls); };

addClass('div_id_placaPatente', 'col-md-4');
addClass('div_id_rutPropietario', 'col-md-4');
addClass('div_id_tenencia', 'col-md-4');
addClass('div_id_nombrePropietario', 'col-md-4');
addClass('div_id_domicilio', 'col-md-4');
addClass('div_id_tipo', 'col-md-4');
addClass('div_id_ano', 'col-md-4');
addClass('div_id_marca', 'col-md-4');
addClass('div_id_modelo', 'col-md-4');
addClass('div_id_numeroMotor', 'col-md-4');
addClass('div_id_numeroChasis', 'col-md-4');
addClass('div_id_numeroVin', 'col-md-4');
addClass('div_id_color', 'col-md-4');
addClass('div_id_fechaVencimientoPermisoCirculacion', 'col-md-4');
addClass('div_id_fechaVencimientoRevisionTecnica', 'col-md-4');
addClass('div_id_fechaVencimientoSeguroObligatorio', 'col-md-4');
addClass('div_id_kilometraje_actual', 'col-md-4');
addClass('div_id_kilometraje_ultima_mantencion', 'col-md-4');
addClass('div_id_frecuencia_mantenimiento', 'col-md-4');

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
