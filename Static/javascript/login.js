document.addEventListener('DOMContentLoaded',()=>{
            
    const username = document.querySelector('#floatingInput')
    const password = document.querySelector('#floatingPassword')
    const inform = document.querySelector('#inform')

    document.querySelector('#login').onclick = async function(event){
        const formData = new FormData();
        formData.append('username', username.value);
        formData.append('password', password.value);
        try{
            const access = await fetch('/success',{
                method: 'POST',
                body: formData
            })
            const message = await access.json();

            if(message.success){
                inform.innerHTML = `<div class='alert alert-primary'style="display:block" id='danger' role='alert'>${message.message}</div>`;
                setTimeout(function () {
                    window.location.href = `/home`
                }, 1000);

            }else{
                inform.innerHTML = `<div class='alert alert-danger'style="display:block" id='danger' role='alert'>${message.message}</div>`;
            }

        }
        catch(error){
            console.error('Error:', error);
        }
    }
})