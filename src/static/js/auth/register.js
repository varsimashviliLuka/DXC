// static/js/auth/register.js

// static/js/auth/check-auth.js

document.addEventListener("DOMContentLoaded", async () => {

    const loggedIn = await isAuthenticated();

    if (loggedIn) {

        // User already logged in
        window.location.href = "/";
    }

    const registerForm = document.getElementById("registerForm");
const message = document.getElementById("message");

registerForm.addEventListener("submit", async (e) => {

    e.preventDefault();

    const email =
        document.getElementById("email").value;

    const phoneNumber =
        document.getElementById("phone_number").value;

    const personalNumber =
        document.getElementById("personal_number").value;

    const password =
        document.getElementById("password").value;

    const passwordRepeat =
        document.getElementById("passwordRepeat").value;

    // Password match validation
    if (password !== passwordRepeat) {

        message.textContent =
            "Passwords do not match.";

        message.style.color = "red";

        return;
    }

    try {

        const response = await sendRequest(
            "/api/auth/registration",
            {
                method: "POST",

                body: JSON.stringify({
                    email: email,
                    phone_number: phoneNumber,
                    personal_number: personalNumber,
                    password: password,
                    passwordRepeat: passwordRepeat
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            message.textContent =
                "Registration successful.";

            message.style.color = "green";

            // Optional auto redirect
            setTimeout(() => {
                window.location.href = "/login";
            }, 1500);

        } else {

            message.textContent =
                data.error || "Registration failed.";

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

