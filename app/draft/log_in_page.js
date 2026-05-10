// Function that changes the display of the SignUpForm to show it
function popupSignup() {
    document.getElementById("SignUpForm").style.display = "flex";
}

// Function that changes the display of the SignUpForm to hide it.
function closeSignUp() {
    document.getElementById("SignUpForm").style.display = "none";
}

// This is a function that closes the popup when the user clicks on the background
window.onclick = function(event) {
    let modal = document.getElementById("SignUpForm");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

//This js is completed by Keithlin it should be working when used...