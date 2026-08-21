function updateImages(inputElement, imagenElement, hrefElement) {
    inputElement.addEventListener("change", () => {
        const archivos = inputElement.files;
        if (!archivos || !archivos.length) {
            imagenElement.src = objectURL;
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

if (document.querySelector("#fotografiaUsuario")){
    updateImages(
        document.querySelector("#fotografiaUsuario"),
        document.querySelector("#imagenUsuario"),
        document.querySelector("#hrefUsuario"),
    );
}
if (document.querySelector("#fotografiaCedula")){
    updateImages(
        document.querySelector("#fotografiaCedula"),
        document.querySelector("#imagenCedula"),
        document.querySelector("#hrefCedula"),
    );
}
if (document.querySelector("#fotografiaLicencia")){
    updateImages(
        document.querySelector("#fotografiaLicencia"),
        document.querySelector("#imagenLicencia"),
        document.querySelector("#hrefLicencia"),
    );
}
if (document.querySelector("#fotografiaLicenciaInterna")){
    updateImages(
        document.querySelector("#fotografiaLicenciaInterna"),
        document.querySelector("#imagenLicenciaInterna"),
        document.querySelector("#hrefLicenciaInterna"),
    );
}
if (document.querySelector("#archivoDocumento")){
    updateImages(
        document.querySelector("#archivoDocumento"),
        document.querySelector("#imagenDocumento"),
        document.querySelector("#hrefDocumento"),
    );
}

function toggleSwitch(elementId) {
    var checkBox = document.getElementById(elementId);
    if (checkBox.checked == true){
        checkBox.setAttribute('value', "si");        
    } else {
        checkBox.setAttribute('value', "no");
    }
}