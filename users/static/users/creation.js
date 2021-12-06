document.addEventListener("DOMContentLoaded", () => {
    // get the button
    document.querySelector(".showPasswordCreatingAccount").onclick = () =>{
        
        if (document.querySelector(".showPasswordCreatingAccount").innerHTML === "Show")
        {
            document.querySelector(".showPasswordCreatingAccount").innerHTML = "Hide";
            document.querySelector("#passwordInput").type = "text";
        }else {
            document.querySelector(".showPasswordCreatingAccount").innerHTML = "Show";
            document.querySelector("#passwordInput").type = "password";
        }
    }
    document.querySelector("#confirm").onclick = () =>{
        
        if (document.querySelector("#confirm").innerHTML === "Show")
        {
            document.querySelector("#confirm").innerHTML = "Hide";
            document.querySelector("#confrimUserPassword").type = "text";
        }else {
            document.querySelector("#confirm").innerHTML = "Show";
            document.querySelector("#confrimUserPassword").type = "password";
        }
    }
    // for when the passswords dont match
    document.querySelector("#signUpProperties").onclick = () => {
        if (document.querySelector("#confrimUserPassword").value === document.querySelector("#passwordInput"))
        {
            return true;
        }
        alert("Your passwords dont match")
        return false;
    }
})