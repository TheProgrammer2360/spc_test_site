document.addEventListener("DOMContentLoaded", () => {
    
    document.querySelector(".showPassword").addEventListener("click", () => {
        // put the button is a variable
        let passButton = document.querySelector(".showPassword");
        // put the the password as a variable
        let passArea = document.querySelector(".userPassword");
        if (passButton.innerHTML === "Show"){
            passButton.innerHTML = "Hide";
            passArea.type = "text";
        }else{
            passButton.innerHTML = "Show";
            passArea.type = "password";
        }
    })
})