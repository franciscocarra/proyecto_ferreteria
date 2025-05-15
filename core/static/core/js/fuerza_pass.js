document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.querySelector("#password");
    const strengthText = document.querySelector("#password-strength");

    passwordInput.addEventListener("input", function () {
        const password = passwordInput.value;
        const strength = getPasswordStrength(password);

        // Cambiar texto y color según fuerza
        strengthText.textContent = `Fuerza de la contraseña: ${strength.label}`;
        strengthText.style.color = strength.color;
    });

    function getPasswordStrength(password) {
        let score = 0;

        if (password.length >= 8) score++;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
        if (/\d/.test(password)) score++;
        if (/[^a-zA-Z0-9]/.test(password)) score++;

        if (score <= 1) {
            return { label: "Débil", color: "red" };
        } else if (score === 2 || score === 3) {
            return { label: "Fuerte", color: "green" };
        } 
        
    }
});