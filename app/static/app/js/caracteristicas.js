document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageElement = document.getElementById('message');

    if (username === 'usuario' && password === 'contraseña') {
        messageElement.style.color = 'green';
        messageElement.textContent = 'Login exitoso!';
    } else {
        messageElement.style.color = 'red';
        messageElement.textContent = 'Usuario o contraseña incorrectos.';
    }
});