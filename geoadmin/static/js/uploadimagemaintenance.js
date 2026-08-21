function toggleSwitch(elementId) {
    var checkBox = document.getElementById(elementId);
    if (checkBox.checked == true){
        checkBox.setAttribute('value', "si");        
    } else {
        checkBox.setAttribute('value', "no");
    }
}

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

if (document.querySelector("#fotografiaUno")){
    updateImages(
        document.querySelector("#fotografiaUno"),
        document.querySelector("#imagenUno"),
        document.querySelector("#hrefUno"),
    );
}
if (document.querySelector("#fotografiaDos")){
    updateImages(
        document.querySelector("#fotografiaDos"),
        document.querySelector("#imagenDos"),
        document.querySelector("#hrefDos"),
    );
}
if (document.querySelector("#fotografiaTres")){
    updateImages(
        document.querySelector("#fotografiaTres"),
        document.querySelector("#imagenTres"),
        document.querySelector("#hrefTres"),
    );
}
