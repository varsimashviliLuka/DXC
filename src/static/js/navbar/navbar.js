const loginLink = document.getElementById("loginLink");
const registerLink = document.getElementById("registerLink");

const userSection = document.getElementById("userSection");
const logoutBtn = document.getElementById("logoutBtn");

async function updateNavbar() {

    try {

        // Try to fetch current user
        const response = await sendRequest("/api/user/myuser", {
            method: "GET"
        });

        if (response.ok) {

            const data = await response.json();

            console.log("Logged in user:", data);

            // Hide login/register
            loginLink.style.display = "none";
            registerLink.style.display = "none";

            // Show logout
            userSection.style.display = "block";

        } else {

            throw new Error("Not logged in");
        }

    } catch (error) {

        // Not authenticated

        loginLink.style.display = "inline";
        registerLink.style.display = "inline";

        userSection.style.display = "none";
    }
}

// Run on page load
document.addEventListener("DOMContentLoaded", updateNavbar);

// Logout handler
logoutBtn.addEventListener("click", async () => {

    await logout(); // your existing logout function
});