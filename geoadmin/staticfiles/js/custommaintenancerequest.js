document.getElementById('div_id_solicitante').classList.add('col-md-4');
document.getElementById('div_id_telefono').classList.add('col-md-4');
document.getElementById('div_id_turno').classList.add('col-md-4');
document.getElementById('div_id_vehiculo').classList.add('col-md-4');
document.getElementById('div_id_kilometraje').classList.add('col-md-4');
//document.getElementById('div_id_avisoJefatura').classList.add('col-md-4');
document.getElementById('div_id_problemas').classList.add('col-md-8');
document.getElementById('div_id_comentario').classList.add('col-md-8');
document.getElementById('div_id_progreso').classList.add('col-md-4');
document.getElementById('div_id_empresaMantenimiento').classList.add('col-md-4');

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
