'use strict'
const clientList = document.querySelector('#clientList')

clientList.addEventListener('change', (evt) => {
  evt.preventDefault();
  console.log(clientList);
  
    const clientId = document.getElementById('clientList').value
    console.log(clientId)
  
    window.location.href = `/clients/${clientId}`
})

console.log('fuck', clientList)
// clientList.addEventListener('change', (evt) => {
//   evt.preventDefault();
//   console.log(clientList.options)


// })

