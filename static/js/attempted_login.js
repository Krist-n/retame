'use strict'

$.get('/attempted_login', (res) => {

    if (res != null) {

        Toastify({

            text: res,
            duration: 5000,
            backgroundColor: "linear-gradient(to right, #083248, #d4af37",
            newWindow: true,
            close: true

                
        }).showToast();
    }
 });