'use strict'

$.get('/logout_user', (res) => {

    if (res != null) {

        Toastify({

            text: res,
            duration: 3000,
            backgroundColor: "linear-gradient(to right, #083248, #d4af37",
            newWindow: true,
            close: false

        }).showToast();
    }
})