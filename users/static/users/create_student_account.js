document.addEventListener("DOMContentLoaded", () => {
    // getting the button object
    const showButton = document.querySelector("#show");
    // click event on the button
    showButton.onclick = () => {
        // getting the password object
        const passwordInstance = document.querySelector("#password");
        if (showButton.innerHTML === "show"){
            passwordInstance.type = "text";
            showButton.innerHTML = "hide"
        }else {
            passwordInstance.type = "password";
            showButton.innerHTML = "show";
        }
    }
})