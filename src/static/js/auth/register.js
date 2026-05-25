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

    function setMessage(text, color = "red") {
        message.textContent = text;
        message.style.color = color;
    }

    function getApiError(data, fallbackMessage) {
        if (data?.error) {
            return data.error;
        }
        if (data?.message && typeof data.message === "string") {
            return data.message;
        }
        if (data?.errors && typeof data.errors === "object") {
            const firstField = Object.keys(data.errors)[0];
            if (firstField && Array.isArray(data.errors[firstField])) {
                return data.errors[firstField][0];
            }
            if (firstField && typeof data.errors[firstField] === "string") {
                return data.errors[firstField];
            }
        }

        return fallbackMessage;
    }

    registerForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const email =
            document.getElementById("email").value.trim();

        const rawPhoneNumber =
            document.getElementById("phone_number").value.trim();

        const rawPersonalNumber =
            document.getElementById("personal_number").value.trim();

        const password =
            document.getElementById("password").value;

        const passwordRepeat =
            document.getElementById("passwordRepeat").value;

        const personalNumber =
            rawPersonalNumber.replace(/\D/g, "");

        let phoneNumber =
            rawPhoneNumber.replace(/\D/g, "");

        // Accept +995xxxxxxxxx and convert to local 9-digit format.
        if (phoneNumber.length === 12 && phoneNumber.startsWith("995")) {
            phoneNumber = phoneNumber.slice(3);
        }

        if (phoneNumber.length !== 9) {
            setMessage("Phone number must contain 9 digits (or start with +995).");
            return;
        }

        if (personalNumber.length !== 11) {
            setMessage("Personal number must contain exactly 11 digits.");
            return;
        }

        // Password match validation
        if (password !== passwordRepeat) {
            setMessage("Passwords do not match.");
            return;
        }

        try {

            const response = await sendRequest(
                "/api/auth/registration",
                {
                    method: "POST",

                    body: JSON.stringify({
                        email,
                        phone_number: phoneNumber,
                        personal_number: personalNumber,
                        password,
                        passwordRepeat
                    })
                }
            );

            const data = await response.json();

            if (response.ok) {

                setMessage("Registration successful.", "green");

                // Optional auto redirect
                setTimeout(() => {
                    window.location.href = "/login";
                }, 1500);

            } else {
                setMessage(getApiError(data, "Registration failed."));
            }

        } catch (error) {

            console.error(error);

            setMessage("Something went wrong.");
        }
    });

});

