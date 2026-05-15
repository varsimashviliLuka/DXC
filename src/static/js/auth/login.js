document.addEventListener("DOMContentLoaded", async () => {

    const loggedIn = await isAuthenticated();

    if (loggedIn) {

        // User already logged in
        window.location.href = "/";
    }

    const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");

loginForm.addEventListener("submit", async (e) => {

    e.preventDefault();

    const emailOrPhone =
        document.getElementById("email_or_phone_number").value;

    const password =
        document.getElementById("password").value;

    try {

        const response = await sendRequest("/api/auth/login", {
            method: "POST",

            body: JSON.stringify({
                email_or_phone_number: emailOrPhone,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {

            // Save access token
            localStorage.setItem(
                "access_token",
                data.access_token
            );

            message.textContent =
                "Login successful!";

            message.style.color = "green";

            // Redirect
            window.location.href = "/";

        } else {

            message.textContent =
                data.error || "Login failed.";

            message.style.color = "red";
        }

    } catch (error) {

        console.error(error);

        message.textContent =
            "Something went wrong.";

        message.style.color = "red";
    }
});

});

