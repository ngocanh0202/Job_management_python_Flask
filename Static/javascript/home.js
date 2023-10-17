document.addEventListener('DOMContentLoaded',()=>{
    const showPasswordButton = document.querySelectorAll('.showPasswordButton')
    const passwordInput = document.querySelectorAll('.password')
    showPasswordButton.forEach((button,index) => {
        button.addEventListener('click',function(){
            const password = passwordInput[index]
            if (password.type === 'password') {
                password.type = 'text';
            } else {
                password.type = 'password';
            }
        })
    })
})    