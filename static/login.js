// login.js - show/hide password toggle (DOM manipulation).
// Demonstrates: selecting elements, handling a "click" event, and
// changing an element's attribute/text with JavaScript.

document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('toggle-password');
    const password = document.getElementById('password');
    if (!toggle || !password) return;

    toggle.addEventListener('click', function () {
        if (password.type === 'password') {
            password.type = 'text';   // reveal the password
            toggle.textContent = 'Hide';
        } else {
            password.type = 'password'; // hide it again
            toggle.textContent = 'Show';
        }
    });
});
