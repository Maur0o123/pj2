document.getElementById('div_id_placaPatente').classList.add('col-md-4');
document.getElementById('div_id_rutPropietario').classList.add('col-md-4');
document.getElementById('div_id_tenencia').classList.add('col-md-4');
if (document.getElementById('div_id_fechaAdquisicion')) {document.getElementById('div_id_fechaAdquisicion').classList.add('col-md-4');}
if (document.getElementById('div_id_fechaArriendoInicial')) {document.getElementById('div_id_fechaArriendoInicial').classList.add('col-md-4');}
if (document.getElementById('div_id_fechaArriendoFinal')) {document.getElementById('div_id_fechaArriendoFinal').classList.add('col-md-4');}
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
document.getElementById('div_id_fechaVencimientoLamina').classList.add('col-md-4');
document.getElementById('div_id_fechaInstalacionBarraAntiVuelco').classList.add('col-md-4');
document.getElementById('div_id_fechaInstalacionGps').classList.add('col-md-4');
document.getElementById('div_id_fechaCertificadoOperatividad').classList.add('col-md-4');
document.getElementById('div_id_fechaCertificadoMantencion').classList.add('col-md-4');
document.getElementById('div_id_fechaCertificadoGrua').classList.add('col-md-4');
document.getElementById('div_id_fechaVencimientoTransportePrivado').classList.add('col-md-4');
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
document.getElementById('div_id_dispositivo').classList.add('col-md-4');
document.getElementById('div_id_proveedor').classList.add('col-md-4');


function selectTenencia(tenencia){
    if (tenencia == 'Propio'){
        document.getElementById('div_id_fechaAdquisicion').classList.remove('oculto');
        $('#div_id_fechaAdquisicion').show();
        $('#div_id_fechaArriendoInicial').hide();
        $('#div_id_fechaArriendoFinal').hide();
    }
    if (tenencia == 'Arrendado'){
        document.getElementById('div_id_fechaAdquisicion').classList.add('oculto');
        $('#div_id_fechaAdquisicion').hide();
        $('#div_id_fechaArriendoInicial').show();
        $('#div_id_fechaArriendoFinal').show();
    }
    if (tenencia == '---------'){
        document.getElementById('div_id_fechaAdquisicion').classList.add('oculto');
        $('#div_id_fechaAdquisicion').hide();
        $('#div_id_fechaArriendoInicial').hide();
        $('#div_id_fechaArriendoFinal').hide();
    }
}

function toggleSwitch(elementId) {
    var checkBox = document.getElementById(elementId);
    if (checkBox.checked == true){
        checkBox.setAttribute('value', "si");        
    } else {
        checkBox.setAttribute('value', "no");
    }
}

const inputs = document.querySelectorAll('input');
const textareas = document.querySelectorAll('textarea');
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
textareas.forEach(ctrl => {
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


$(document).ready(function() {
    var texto = $('#id_tipo').find('option:selected').text();
    ocultarOpciones(texto);    
    $('#id_tipo').change(function(){
        var tipo_texto = $(this).find('option:selected').text();
        ocultarOpciones(tipo_texto);       
    });
});

function hideoptions(opciones){
    var opciones = opciones;
    var informaciontecnica = 0;
    var documentacion = 0;
    var exterior = 0;
    var interior = 0;
    var propiedadesInformacionTecnica = ["tipoTraccion", "pesoBrutoVehicular", "capacidadCarga", "tipoNeumatico", "tipoAceiteMotor", "tipoRefrigeranteMotor", "tipoFiltroAireMotor", "tipoFiltroCombustible", "frecuenciaMantenimiento", "proximoMantenimiento", "proximoMantenimientoGrua"];
    var propiedadesDocumentacion = ["fotografiaFacturaCompra", "fotografiaPadron", "fotografiaPermisoCirculacion", "fotografiaRevisionTecnica", "fotografiaRevisionTecnicaGases", "fotografiaSeguroObligatorio", "fotografiaSeguroAutomotriz", "fotografiaCertificadoGps", "fotografiaCertificadoMantencion", "fotografiaCertificadoOperatividad",  "fotografiaCertificadoGrua", "fotografiaCertificadoLamina", "fotografiaCertificadoBarraAntiVuelco", "fotografiaDocumentacionMiniBus"];
    var propiedadesExterior = ["fotografiaExteriorFrontis", "fotografiaExteriorPiloto", "fotografiaExteriorCopiloto", "fotografiaExteriorAtras"];
    var propiedadesInterior = ["fotografiaInteriorTablero", "fotografiaInteriorCopiloto", "fotografiaInteriorAtrasPiloto", "fotografiaInteriorAtrasCopiloto"]
    $('#div_id_informacionTecnica').show();
    $('#div_id_fotografiasDocumentacion').show();
    $('#div_id_fotografiasExterior').show();
    $('#div_id_fotografiasInterior').show();
    for (var propiedad in opciones) {
        if (opciones.hasOwnProperty(propiedad)) {
            var valor = opciones[propiedad].toLowerCase();
            if (valor == "si"){
                $('#div_id_'+propiedad).show();
            } else { 
                $('#div_id_'+propiedad).hide();
                if (propiedadesInformacionTecnica.includes(propiedad)) {
                    informaciontecnica += 1;
                };
                if (propiedadesDocumentacion.includes(propiedad)) {
                    documentacion += 1;
                };
                if (propiedadesExterior.includes(propiedad)) {
                    exterior += 1;
                };
                if (propiedadesInterior.includes(propiedad)) {
                    interior += 1;
                };
            };
        };
    };
    if (informaciontecnica == propiedadesInformacionTecnica.length){
        $('#div_id_informacionTecnica').hide();
    };
    if (documentacion == propiedadesDocumentacion.length){
        $('#div_id_fotografiasDocumentacion').hide();
    };
    if (exterior == propiedadesExterior.length){
        $('#div_id_fotografiasExterior').hide();
    };
    if (interior == propiedadesInterior.length){
        $('#div_id_fotografiasInterior').hide();
    };
}

$(document).ready(function() {
    var tenencia_texto = $('#id_tenencia').find('option:selected').text();
    selectTenencia(tenencia_texto);
    $('#id_tenencia').change(function(){
        var tenencia = $(this).find('option:selected').text();
        selectTenencia(tenencia);
    });
});
