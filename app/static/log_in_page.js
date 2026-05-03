function popupSignup() {
    document.getElementById("SignUpForm").style.display = "flex";
}

function closeSignUp() {
    document.getElementById("SignUpForm").style.display = "none";
}

window.onclick = function(event) {
    let modal = document.getElementById("SignUpForm");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
