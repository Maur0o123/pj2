function addClass(id, cls) {
    var el = document.getElementById(id);
    if (el) el.classList.add(cls);
}

addClass('div_id_maquinaria', 'col-md-4');
addClass('div_id_descripcion', 'col-md-4');
addClass('div_id_fechaAdquisicion', 'col-md-4');
addClass('div_id_tipo', 'col-md-4');
addClass('div_id_marca', 'col-md-4');
addClass('div_id_faena', 'col-md-4');
addClass('div_id_frecuenciaMantenimiento', 'col-md-4');
addClass('div_id_horometro_actual', 'col-md-4');
addClass('div_id_horometro_ultima_mantencion', 'col-md-4');

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
