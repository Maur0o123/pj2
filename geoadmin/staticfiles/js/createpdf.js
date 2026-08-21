
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
function handleFormSubmit(event, url) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    $.ajax({
        url: pdfViewUrl, 
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() },
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.pdf_url) {
                Swal.fire({
                    icon: 'success',
                    title: 'Documento Creado!',
                    text: 'Presiona "OK" para descargar',
                    confirmButtonColor: '#ff00d9',
                }).then(() => {
                    var link = document.createElement('a');
                    link.href = response.pdf_url;
                    link.download = response.pdf_url.split('/').pop();
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                });
            } else if (response.error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al Crear Documento',
                    text: 'Vuelva a intentarlo!',
                    confirmButtonColor: '#ff00d9',
                });
            }
        },
        error: function() {
            Swal.fire({
                icon: 'error',
                title: 'Error al Crear Documento',
                text: 'Vuelva a intentarlo!',
                confirmButtonColor: '#ff00d9',
            });
        }
    });
}
function registerFormSubmit(classForm) {
    const forms = document.querySelectorAll(classForm);
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
}
function updateCsrfAndRegister(classForm) {
    const csrfToken = getCsrfToken();
    document.querySelectorAll(classForm + '').forEach(form => {
        form.querySelector('input[name="csrfmiddlewaretoken"]').value = csrfToken;
    });
    registerFormSubmit(classForm);
}
document.addEventListener('DOMContentLoaded', function() {
    const table = $(idDataTable).DataTable({
        language: {
            url: urlLenguage,
        },
        responsive: {
            details: {
                type: 'column',
                target: 0
            }
        },
        scrollX: false,
        autoWidth: false,
        columnDefs: [
            { className: 'dtr-control', orderable: false, targets: 0, width: "30px" },
            { searchable: false, targets: [0, -1] },
            { orderable: false, targets: [0, -1] }
        ]
    });
    registerFormSubmit(classForm);
    $(idDataTable).on('draw.dt', function() {
        registerFormSubmit(classForm);
    });
    $(idDataTable).on('click', '.dtr-control', function() {
        updateCsrfAndRegister(classForm);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    if (typeof idDataTableDes !== 'undefined' && idDataTableDes) {
        const table = $(idDataTableDes).DataTable({
            language: {
                url: urlLenguage,
            },
            responsive: {
                details: {
                    type: 'column',
                    target: 0
                }
            },
            scrollX: false,
            autoWidth: false,
            columnDefs: [
                { className: 'dtr-control', orderable: false, targets: 0, width: "30px" },
                { searchable: false, targets: [0, -1] },
                { orderable: false, targets: [0, -1] }
            ]
        });
        registerFormSubmit(classForm);
        $(idDataTableDes).on('draw.dt', function() {
            registerFormSubmit(classForm);
        });
        $(idDataTableDes).on('click', '.dtr-control', function() {
            updateCsrfAndRegister(classForm);
        });
    }
});

// Recalcular dimensiones de DataTables al cambiar de pestaña
$(document).ready(function() {
    $('a[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust().responsive.recalc();
    });
});