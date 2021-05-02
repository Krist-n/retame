'use strict'

const logoutNav = document.querySelector('#logout')
logoutNav.addEventListener('click', (evt) => {
    evt.preventDefault();

    
    $.post("/logout", ()  => {
        console.log("HIIIIIIIIIIIIIIII")
        // window.location.replace('/')
    })
    
    window.location.replace('/')

})

