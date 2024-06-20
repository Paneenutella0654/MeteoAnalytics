const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	window.location.href = '/register';
});

signInButton.addEventListener('click', () => {
	window.location.href = '/login';
});