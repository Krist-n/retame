'use strict'

$.get('/isloggedin', (res) => {

    if (res != null) {
        // console.log(res)
        Toastify({
            
            text: res,
            duration: 8000,
            // backgroundColor: "linear-gradient(to right, #2e8a, #ebccda",
            newWindow: true,
            close: false,

        }).showToast();
    }
})        
    
        
        
            // setTimeout(() => {window.location.href='/user    _homepage'}, 4000);
            
        // } else {

        //     Toastify({

        //         text: "Incorrect email or password",
        //         duration: 3000,
        //         backgroundColor: "linear-gradient(to right, #f22e8a, #ebccda",
        //         newWindow: true,
        //         close: false,
            
        //     }).showToast();
            
        //     setTimeout(() => {window.location.href='/'}, 4000);
        // }        
               
