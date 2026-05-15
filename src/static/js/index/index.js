if (window.authUser){
    console.log("User is authenticated:", window.authUser);
}

const getUserButton =
    document.getElementById("getUserButton");

const userData =
    document.getElementById("userData");

getUserButton.addEventListener("click", async () => {

    if (window.authUser){
        userData.textContent = JSON.stringify(window.authUser, null, 4);
    }else{
        userData.textContent = "No authenticated user.";
    }

});