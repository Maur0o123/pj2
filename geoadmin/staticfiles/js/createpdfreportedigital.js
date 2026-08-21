function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Función principal para generar el PDF
function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    $.LoadingOverlay("show");

    $.ajax({
        url: pdfViewUrl, // Variable global definida en el template
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() }, // Enviamos el token en el header (más seguro y robusto para Django)
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $.LoadingOverlay("hide");
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
                Swal.fire({ icon: 'error', title: 'Error al Crear Documento', text: 'Vuelva a intentarlo!', confirmButtonColor: '#ff00d9' });
            }
        },
        error: function(error) {
            $.LoadingOverlay("hide");
            Swal.fire({ icon: 'error', title: 'Error de Conexión', text: 'Vuelva a intentarlo!', confirmButtonColor: '#ff00d9' });
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const table = new DataTable(idDataTable, {
        serverSide: true, 
        processing: true, 
        ajax: {
            url: dataUrl,
            type: 'GET'
        },
        columns: [
            { data: null, defaultContent: '', className: 'dtr-control', orderable: false },
            { data: 'id_checklist' },
            { data: 'fecha' },
            { data: 'sondaje' },
            { data: 'sonda' },
            { data: 'creador' },
            { data: 'turno' },
            { data: 'acciones', orderable: false }
        ],
        columnDefs: [
            { searchable: false, targets: [0, 7] },
            { orderable: false, targets: [0, 7] }
        ],
        order: [[2, 'desc']], 
        language: { url: urlLenguage },
        responsive: {
            details: { type: 'column', target: 'td.dtr-control' }
        }
    });

    // --- LÓGICA DE PDF (Delegación de eventos) ---
    // Esto conecta el botón de PDF automáticamente, incluso cuando cambias de página en la tabla
    $(idDataTable).on('submit', classForm, function(event) {
        handleFormSubmit(event);
    });

    // --- LÓGICA DE ELIMINACIÓN ---
    $(idDataTable).on('submit', '.form-delete', function(e) {
        e.preventDefault();
        var form = this;
        var actionUrl = $(form).attr('action');
        var formData = new FormData(form);

        Swal.fire({
            title: '¿Estás seguro?',
            text: "Estás a punto de eliminar un reporte APROBADO. Esta acción lo enviará a la bandeja de eliminados.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.LoadingOverlay("show");
                
                $.ajax({
                    url: actionUrl,
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCsrfToken() },
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(response) {
                        $.LoadingOverlay("hide");
                        
                        if (response.status === 'success') {
                            Swal.fire('Eliminado!', response.message, 'success');
                            // Recargamos la tabla manteniendo la paginación actual
                            table.draw(false); 
                        } else {
                            Swal.fire('No se pudo eliminar', response.message, 'error');
                        }
                    },
                    error: function(xhr) {
                        $.LoadingOverlay("hide");
                        var msg = (xhr.responseJSON && xhr.responseJSON.message) ? xhr.responseJSON.message : 'Error desconocido';
                        Swal.fire('Error', msg, 'error');
                    }
                });
            }
        });
    });
});