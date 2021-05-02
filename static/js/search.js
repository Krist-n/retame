'use strict'
const clientList = document.getElementById('client-details').addEventListener('click', (evt) => {
  evt.preventDefault();
  
  const clientId = document.getElementById('clientList').value
  console.log(clientId)
  
  window.location.href = `/clients/${clientId}`
})





// const searchForm = getElementById('#clientListOptions').addEventListener('click', (evt) => {
//     const searchInput = document.querySelector('input[name="search"]');

//     if (searchInput.value.length < 3) {
//     evt.preventDefault();

//     } else {
//         const results = document.createElement('li');
//         results.innerText(results)
//     }

// }




/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
// function searchFunc() {
//   document.getElementById("search-form").classList.toggle("show");
// }

// function filterFunction() {
//   var input, filter, ul, li, a, i;
//   input = document.getElementById("myInput");
//   filter = input.value.toUpperCase();
//   div = document.getElementById("myDropdown");
//   a = div.getElementsByTagName("a");
//   for (i = 0; i < a.length; i++) {
//     txtValue = a[i].textContent || a[i].innerText;
//     if (txtValue.toUpperCase().indexOf(filter) > -1) {
//       a[i].style.display = "";
//     } else {
//       a[i].style.display = "none";
//     }
//   }
// }
// </script>