'use strict'

$.get('/attempted_login', (res) => {

    if (res != null) {

        Toastify({

            text: res,
            duration: 5000,
            backgroundColor: "linear-gradient(to right, #f22e8a, #ebccda",
            newWindow: true,
            close: true

                
        }).showToast();
    }
 });