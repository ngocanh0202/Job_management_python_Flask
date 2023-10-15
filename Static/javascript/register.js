document.addEventListener('DOMContentLoaded', () => {
    const usernameInput = document.querySelector('#floatingInput');
    const passwordInput = document.querySelector('#floatingPassword');
    const passwordAgainInput = document.querySelector('#floatingPasswordAgain');
    const inform = document.querySelector(".inform");



    document.querySelector("#register").onclick =  async function (event) {
        const formData = new FormData();
        formData.append('username', usernameInput.value);
        formData.append('password', passwordInput.value);
        formData.append('password_again',passwordAgainInput.value)
        try {
            const response = await fetch('/register_check', {
                method: 'POST',
                body: formData,
            });

            const responseData = await response.json();

            if (responseData.success) {
                inform.innerHTML = `<div class='alert alert-primary' style="display:block" id='success' role='alert'>${responseData.message}</div>`;
                setTimeout(function () {
                    var encodedUsername = encodeURIComponent(usernameInput.value);
                    var encodedPassword = encodeURIComponent(passwordInput.value);
                    window.location.href = '/register_success?username='+encodedUsername+'&password='+encodedPassword+''
                }, 1000);
            } else {
                inform.innerHTML = `<div class='alert alert-danger'style="display:block" id='danger' role='alert'>${responseData.message}</div>`;
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

});