'use strict'

import {toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


import React from 'react';
  
// Importing toastify module
// Import toastify css file
// toast-configuration method, 
// it is compulsory method.

  
// This is main function
toast.configure()
function reTameToast(){
    // function which is called when 
    // button is clicked
    const notify = () => {
        toast("Account created, please log in.",
           {position: toast.POSITION.TOP_CENTER})

    }
    
    return (
        <div className="new-account">
            <button onClick={notify}>Submit!</button> 
            </div>
    );
}
   
export default reTameToast;