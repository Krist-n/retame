'use strict'



const userAccount = document.querySelector('#new-account')
userAccount.addEventListener('submit', (evt) => {
    evt.preventDefault();
    
    const userInfo = {
        'fname': $('#fname').val(),
        'lname': $('#lname').val(),
        'email': $('#new-account-email').val(),
        'password': $('#new-account-password').val()
    };

    $.post('/create_user', userInfo, (res) => {
   
        if (res != null) {
            Toastify({

                text: res,
                duration: 3000,
                backgroundColor: "linear-gradient(to right, #083248, #d4af37"
                
            }).showToast()
        } 
    })
})
 

