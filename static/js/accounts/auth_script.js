// Wait for the entire HTML document to be fully loaded and parsed.
document.addEventListener('DOMContentLoaded', () => {

    // --- DOM Element Selections ---
    // Get all the elements we need to interact with from the HTML.
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    
    const loginPrompt = document.getElementById('login-prompt');
    const signupPrompt = document.getElementById('signup-prompt');

    const showSignupBtn = document.getElementById('show-signup-btn');
    const showLoginBtn = document.getElementById('show-login-btn');

    // --- Event Listener for "Join Now" button ---
    // When the user wants to switch to the signup form.
    showSignupBtn.addEventListener('click', () => {
        // Hide the login form and its corresponding prompt text.
        loginForm.classList.add('hidden');
        loginPrompt.classList.add('hidden');
        
        // Show the signup form and its corresponding prompt text.
        signupForm.classList.remove('hidden');
        signupPrompt.classList.remove('hidden');
    });

    // --- Event Listener for "Log In" button ---
    // When the user wants to switch back to the login form.
    showLoginBtn.addEventListener('click', () => {
        // Hide the signup form and its prompt text.
        signupForm.classList.add('hidden');
        signupPrompt.classList.add('hidden');
        
        // Show the login form and its prompt text.
        loginForm.classList.remove('hidden');
        loginPrompt.classList.remove('hidden');
    });

});