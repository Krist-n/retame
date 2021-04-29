'use strict'

$.get('/logout_user', (res) => {

    if (res != null) {

        Toastify({

            text: res,
            duration: 3000,
            backgroundColor: "linear-gradient(135deg, #7d8188, #f1f2f5);",
            newWindow: true,
            close: false

        }).showToast();
    }
})