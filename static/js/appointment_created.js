'use strict'
const apptCreated = document.getElementById('appt-created')
apptCreated.addEventListener('click', (evt) => {
    // evt.preventDefault();
    console.log("hiiiiiiiiiii")
    $.get('/appointment_created', (res) => {


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
})
