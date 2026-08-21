function updateImages(inputElement, imagenElement, hrefElement) {
    inputElement.addEventListener("change", () => {
        const archivos = inputElement.files;
        if (!archivos || !archivos.length) {
            imagenElement.src = "";
            hrefElement.src = "";
            return;
        }
        const primerArchivo = archivos[0];
        const objectURL = URL.createObjectURL(primerArchivo);
        if (/^image\/(png|jpeg|jpg|gif|bmp|svg\+xml)$/.test(primerArchivo.type)) {
            imagenElement.src = objectURL;
            hrefElement.href = objectURL;
        } else if (primerArchivo.type === "application/pdf") {
            const imagenRepresentativa = "/static/images/base/archivo-pdf.png";
            imagenElement.src = imagenRepresentativa;        
            hrefElement.href = objectURL;       
        } else {
            const imagenRepresentativa = "/static/images/base/archivo-otro.png";
            imagenElement.src = imagenRepresentativa;
            hrefElement.href = objectURL;        
        }
    });
}

if (document.querySelector("#fotografiaPadron")){
    updateImages(
        document.querySelector("#fotografiaPadron"),
        document.querySelector("#imagenPadron"),
        document.querySelector("#hrefPadron"),
        );
}
if (document.querySelector("#fotografiaPermisoCirculacion")){
    updateImages(
        document.querySelector("#fotografiaPermisoCirculacion"),
        document.querySelector("#imagenPermisoCirculacion"),
        document.querySelector("#hrefPermisoCirculacion"),
    );
}
if (document.querySelector("#fotografiaRevisionTecnica")){
    updateImages(
        document.querySelector("#fotografiaRevisionTecnica"),
        document.querySelector("#imagenRevisionTecnica"),
        document.querySelector("#hrefRevisionTecnica"),
    );
}
if (document.querySelector("#fotografiaRevisionTecnicaGases")){
    updateImages(
        document.querySelector("#fotografiaRevisionTecnicaGases"),
        document.querySelector("#imagenRevisionTecnicaGases"),
        document.querySelector("#hrefRevisionTecnicaGases"),
    );
}
if (document.querySelector("#fotografiaSeguroObligatorio")){
    updateImages(
        document.querySelector("#fotografiaSeguroObligatorio"),
        document.querySelector("#imagenSeguroObligatorio"),
        document.querySelector("#hrefSeguroObligatorio"),
    );
}
if (document.querySelector("#fotografiaCertificadoGps")){
    updateImages(
        document.querySelector("#fotografiaCertificadoGps"),
        document.querySelector("#imagenCertificadoGps"),
        document.querySelector("#hrefCertificadoGps"),
    );
}
if (document.querySelector("#fotografiaCertificadoMantencion")){
    updateImages(
        document.querySelector("#fotografiaCertificadoMantencion"),
        document.querySelector("#imagenCertificadoMantencion"),
        document.querySelector("#hrefCertificadoMantencion"),
    );
}
if (document.querySelector("#fotografiaCertificadoOperatividad")){
    updateImages(
        document.querySelector("#fotografiaCertificadoOperatividad"),
        document.querySelector("#imagenCertificadoOperatividad"),
        document.querySelector("#hrefCertificadoOperatividad"),
    );
}
if (document.querySelector("#fotografiaCertificadoGrua")){
    updateImages(
        document.querySelector("#fotografiaCertificadoGrua"),
        document.querySelector("#imagenCertificadoGrua"),
        document.querySelector("#hrefCertificadoGrua"),
    );
}
if (document.querySelector("#fotografiaFacturaCompra")){
    updateImages(
        document.querySelector("#fotografiaFacturaCompra"),
        document.querySelector("#imagenFacturaCompra"),
        document.querySelector("#hrefFacturaCompra"),
    );
}

if (document.querySelector("#fotografiaSeguroAutomotriz")){
    updateImages(
        document.querySelector("#fotografiaSeguroAutomotriz"),
        document.querySelector("#imagenSeguroAutomotriz"),
        document.querySelector("#hrefSeguroAutomotriz"),
    );
}

if (document.querySelector("#fotografiaCertificadoLamina")){
    updateImages(
        document.querySelector("#fotografiaCertificadoLamina"),
        document.querySelector("#imagenCertificadoLamina"),
        document.querySelector("#hrefCertificadoLamina"),
    );
}

if (document.querySelector("#fotografiaCertificadoBarraAntiVuelco")){
    updateImages(
        document.querySelector("#fotografiaCertificadoBarraAntiVuelco"),
        document.querySelector("#imagenCertificadoBarraAntiVuelco"),
        document.querySelector("#hrefCertificadoBarraAntiVuelco"),
    );
}
if (document.querySelector("#fotografiaDocumentacionMiniBus")){
    updateImages(
        document.querySelector("#fotografiaDocumentacionMiniBus"),
        document.querySelector("#imagenDocumentacionMiniBus"),
        document.querySelector("#hrefDocumentacionMiniBus"),
    );
}
if (document.querySelector("#fotografiaCertificadoVarios")){
    updateImages(
        document.querySelector("#fotografiaCertificadoVarios"),
        document.querySelector("#imagenCertificadoVarios"),
        document.querySelector("#hrefCertificadoVarios"),
    );
}
if (document.querySelector("#fotografiaExteriorFrontis")){
    updateImages(
        document.querySelector("#fotografiaExteriorFrontis"),
        document.querySelector("#imagenExteriorFrontis"),
        document.querySelector("#hrefExteriorFrontis"),
    );
}
if (document.querySelector("#fotografiaExteriorAtras")){
    updateImages(
        document.querySelector("#fotografiaExteriorAtras"),
        document.querySelector("#imagenExteriorAtras"),
        document.querySelector("#hrefExteriorAtras"),
    );
}
if (document.querySelector("#fotografiaExteriorPiloto")){
    updateImages(
        document.querySelector("#fotografiaExteriorPiloto"),
        document.querySelector("#imagenExteriorPiloto"),
        document.querySelector("#hrefExteriorPiloto"),
    );
}
if (document.querySelector("#fotografiaExteriorCopiloto")){
    updateImages(
        document.querySelector("#fotografiaExteriorCopiloto"),
        document.querySelector("#imagenExteriorCopiloto"),
        document.querySelector("#hrefExteriorCopiloto"),
    );
}
if (document.querySelector("#fotografiaInteriorTablero")){
    updateImages(
        document.querySelector("#fotografiaInteriorTablero"),
        document.querySelector("#imagenInteriorTablero"),
        document.querySelector("#hrefInteriorTablero"),
    );
}
if (document.querySelector("#fotografiaInteriorCopiloto")){
    updateImages(
        document.querySelector("#fotografiaInteriorCopiloto"),
        document.querySelector("#imagenInteriorCopiloto"),
        document.querySelector("#hrefInteriorCopiloto"),
    );
}
if (document.querySelector("#fotografiaInteriorAtrasPiloto")){
    updateImages(
        document.querySelector("#fotografiaInteriorAtrasPiloto"),
        document.querySelector("#imagenInteriorAtrasPiloto"),
        document.querySelector("#hrefInteriorAtrasPiloto"),
    );
}
if (document.querySelector("#fotografiaInteriorAtrasCopiloto")){
    updateImages(
        document.querySelector("#fotografiaInteriorAtrasCopiloto"),
        document.querySelector("#imagenInteriorAtrasCopiloto"),
        document.querySelector("#hrefInteriorAtrasCopiloto"),
    );
}
