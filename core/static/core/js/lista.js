$(document).ready(function () {
    $('#tablaUsuarios').DataTable({
        ajax: "{% url 'obtener_datos_usuarios' %}", // URL que retorna los datos en formato JSON
        columns: [
            { data: "id" },
            { data: "empleado" },
            { data: "dni" },
            { data: "cargo" },
            { data: "entrada" },
            { data: "salida" },
            {
                data: null,
                className: "dt-center",
                defaultContent: `
                    <button class="btn btn-danger btn-sm eliminar-btn">
                        <i class="fa fa-trash"></i>
                    </button>`
            }
        ],
        language: {
            lengthMenu: "Mostrar _MENU_ registros",
            zeroRecords: "No se encontraron resultados",
            info: "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            infoEmpty: "Mostrando registros del 0 al 0 de un total de 0 registros",
            infoFiltered: "(filtrado de un total de _MAX_ registros)",
            search: "Buscar:",
            paginate: {
                first: "Primero",
                last: "Último",
                next: "Siguiente",
                previous: "Anterior"
            },
        },
    });

    // Eliminar usuario (simulado)
    $('#tablaUsuarios tbody').on('click', '.eliminar-btn', function () {
        const rowData = $('#tablaUsuarios').DataTable().row($(this).parents('tr')).data();
        alert(`Eliminando usuario con ID: ${rowData.id}`);
    });
});
