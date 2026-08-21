document.getElementById('div_id_fechaVencimientoLamina').classList.add('col-md-4');
document.getElementById('div_id_fechaInstalacionBarraAntiVuelco').classList.add('col-md-4');
document.getElementById('div_id_fechaInstalacionGps').classList.add('col-md-4');
document.getElementById('div_id_fechaVencimientoTransportePrivado').classList.add('col-md-4');
document.getElementById('div_id_fechaCertificadoOperatividad').classList.add('col-md-4');
document.getElementById('div_id_fechaCertificadoMantencion').classList.add('col-md-4');
document.getElementById('div_id_fechaCertificadoGrua').classList.add('col-md-4');
document.getElementById('div_id_tieneTag').classList.add('col-md-4');
document.getElementById('div_id_tarjetaCombustible').classList.add('col-md-4');
document.getElementById('div_id_tipoTraccion').classList.add('col-md-4');
document.getElementById('div_id_pesoBrutoVehicular').classList.add('col-md-4');
document.getElementById('div_id_capacidadCarga').classList.add('col-md-4');
document.getElementById('div_id_tipoNeumatico').classList.add('col-md-4');
document.getElementById('div_id_tipoAceiteMotor').classList.add('col-md-4');
document.getElementById('div_id_tipoRefrigeranteMotor').classList.add('col-md-4');
document.getElementById('div_id_tipoFiltroAireMotor').classList.add('col-md-4');
document.getElementById('div_id_tipoFiltroCombustible').classList.add('col-md-4');
document.getElementById('div_id_frecuenciaMantenimiento').classList.add('col-md-4');
document.getElementById('div_id_proximoMantenimiento').classList.add('col-md-4');
document.getElementById('div_id_proximoMantenimientoGrua').classList.add('col-md-4');
document.getElementById('div_id_fotografiaFacturaCompra').classList.add('col-md-4');
document.getElementById('div_id_fotografiaPadron').classList.add('col-md-4');
document.getElementById('div_id_fotografiaPermisoCirculacion').classList.add('col-md-4');
document.getElementById('div_id_fotografiaRevisionTecnica').classList.add('col-md-4');
document.getElementById('div_id_fotografiaRevisionTecnicaGases').classList.add('col-md-4');
document.getElementById('div_id_fotografiaSeguroObligatorio').classList.add('col-md-4');
document.getElementById('div_id_fotografiaSeguroAutomotriz').classList.add('col-md-4');
document.getElementById('div_id_fotografiaCertificadoGps').classList.add('col-md-4');
document.getElementById('div_id_fotografiaCertificadoOperatividad').classList.add('col-md-4');
document.getElementById('div_id_fotografiaCertificadoMantencion').classList.add('col-md-4');
document.getElementById('div_id_fotografiaCertificadoGrua').classList.add('col-md-4');
document.getElementById('div_id_fotografiaCertificadoLamina').classList.add('col-md-4');
document.getElementById('div_id_fotografiaCertificadoBarraAntiVuelco').classList.add('col-md-4');
document.getElementById('div_id_fotografiaDocumentacionMiniBus').classList.add('col-md-4');
document.getElementById('div_id_fotografiaInteriorTablero').classList.add('col-md-4');
document.getElementById('div_id_fotografiaInteriorCopiloto').classList.add('col-md-4');
document.getElementById('div_id_fotografiaInteriorAtrasPiloto').classList.add('col-md-4');
document.getElementById('div_id_fotografiaInteriorAtrasCopiloto').classList.add('col-md-4');
document.getElementById('div_id_fotografiaExteriorFrontis').classList.add('col-md-4');
document.getElementById('div_id_fotografiaExteriorAtras').classList.add('col-md-4');
document.getElementById('div_id_fotografiaExteriorPiloto').classList.add('col-md-4');
document.getElementById('div_id_fotografiaExteriorCopiloto').classList.add('col-md-4');

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