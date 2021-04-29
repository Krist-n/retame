'use strict'

$.get('/appointment_created', (res) => {


    if (res != null) {

        Toastify({

            text: res,
            duration: 3000,
            // backgroundColor: "linear-gradient(to right, #f22e8a, #ebccda",
            newWindow: true,
            close: false

            
        }).showToast();

    }
})
