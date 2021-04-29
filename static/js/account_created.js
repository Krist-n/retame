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

    $.post('/create_users', userInfo, (res) => {
   
        if (res != null) {
            Toastify({

                text: res,
                duration: 3000,
                // backgroundColor: "linear-gradient(to right, #f22e8a, #ebccda"
                
            }).showToast()
        } 
    })
})
 

