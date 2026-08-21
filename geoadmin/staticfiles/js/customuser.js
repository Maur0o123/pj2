document.getElementById('div_id_username').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_first_name').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_last_name').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_email').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_phone').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_role').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_ciudad').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_nacionalidad').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_genero').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_fechaNacimiento').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_faena').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_fechaCedulaVencimiento').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_fechaLicenciaVencimiento').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_fechaLicenciaInternaVencimiento').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_seccionVehicular').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_seccionSondaje').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_seccionPrevencion').classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_seccionInventario')?.classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_seccionInformacionTecnica')?.classList.add('col-xl-4', 'col-lg-6', 'col-md-6');
document.getElementById('div_id_licenciaClaseB').classList.add('col-md-2');
document.getElementById('div_id_licenciaClaseC').classList.add('col-md-2');
document.getElementById('div_id_licenciaClaseD').classList.add('col-md-2');
document.getElementById('div_id_licenciaClaseE').classList.add('col-md-2');
document.getElementById('div_id_licenciaClaseF').classList.add('col-md-2');
document.getElementById('div_id_licenciaClaseA1').classList.add('col-md-2');
document.getElementById('div_id_licenciaClaseA2').classList.add('col-md-2');
document.getElementById('div_id_licenciaClaseA3').classList.add('col-md-2');
document.getElementById('div_id_licenciaClaseA4').classList.add('col-md-2');
document.getElementById('div_id_licenciaClaseA5').classList.add('col-md-2');
document.getElementById('div_id_licenciaClaseA1Antigua').classList.add('col-md-3');
document.getElementById('div_id_licenciaClaseA2Antigua').classList.add('col-md-3');


function toggleSwitch(elementId) {
    var checkBox = document.getElementById(elementId);
    if (checkBox.checked == true){
        checkBox.setAttribute('value', "si");        
    } else {
        checkBox.setAttribute('value', "no");
    }
}


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


function formatUsuario(id_username)
{id_username.value=id_username.value.replace(/[.-]/g, '')
.replace( /^(\d{1,2})(\d{3})(\d{3})(\w{1})$/, '$1.$2.$3-$4')}


function formatTelefono(id_telefono)
{id_telefono.value=id_telefono.value.replace(/[-]/g, '')
.replace( /^(\d{1})(\d{4})(\d{4})$/, '$1$2$3')}
