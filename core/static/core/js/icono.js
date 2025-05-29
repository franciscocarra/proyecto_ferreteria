document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('userMenuButton');
    const dropdown = document.getElementById('userMenuDropdown');

    if (!button || !dropdown) return;

    // Mostrar / ocultar menú al hacer click en el botón
    button.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdown.classList.toggle('hidden');
    });

    // Cerrar menú si clic fuera
    document.addEventListener('click', function() {
        if (!dropdown.classList.contains('hidden')) {
            dropdown.classList.add('hidden');
        }
    });
});