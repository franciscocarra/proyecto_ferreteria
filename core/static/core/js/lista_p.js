function mostrarSeccion(seccion) {
        document.getElementById("bodega-section").style.display = "none";
        document.getElementById("productos-section").style.display = "none";

        if (seccion === 'inventario') {
            document.getElementById("productos-section").style.display = "block";
            document.getElementById("titulo-seccion").textContent = "Inventario de Productos";
        } else if (seccion === 'entradas') {
            // Aquí puedes agregar lógica para mostrar entradas si lo deseas
        } else if (seccion === 'salidas') {
            // Aquí puedes agregar lógica para mostrar salidas si lo deseas
        }
    }

    function volverPanel() {
        document.getElementById("bodega-section").style.display = "block";
        document.getElementById("productos-section").style.display = "none";
        document.getElementById("titulo-seccion").textContent = "Panel del Bodeguero";
    }
