document.addEventListener("DOMContentLoaded", function () {
    const btnCrear = document.getElementById("btn-crear-producto");
    const listaProductos = document.getElementById("lista-productos");
    const formularioCrear = document.getElementById("formulario-crear-producto");
    const btnCancelar = document.getElementById("btn-cancelar");

    if (btnCrear && listaProductos && formularioCrear && btnCancelar) {
        btnCrear.addEventListener("click", function () {
            listaProductos.style.display = "none";
            formularioCrear.style.display = "block";
        });

        btnCancelar.addEventListener("click", function () {
            formularioCrear.style.display = "none";
            listaProductos.style.display = "block";
        });
    }
});