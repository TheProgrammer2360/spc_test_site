document.addEventListener("DOMContentLoaded", () => {
    // getting the button object
    const showButton = document.querySelector("#show");
    // click event on the button
    const passwordInstance = document.querySelector("#password");
    showButton.onclick = () => {
        // getting the password object
        if (showButton.innerHTML === "show"){
            passwordInstance.type = "text";
            showButton.innerHTML = "hide";
        }else {
            passwordInstance.type = "password";
            showButton.innerHTML = "show";
        }
    }
    // adding the password strength meter
    passwordInstance
})