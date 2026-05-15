const navbarAuth =
    document.getElementById("navbarAuth");

const guestSection =
    document.getElementById("guestSection");

const userSection =
    document.getElementById("userSection");


const adminLink =
    document.getElementById("adminLink");

const logoutBtn =
    document.getElementById("logoutBtn");


// Global user state
window.authUser = null;


async function initializeNavbar() {

    try {

        const response = await sendRequest(
            "/api/user/myuser",
            {
                method: "GET"
            }
        );

        if (!response.ok) {
            throw new Error("Unauthorized");
        }

        const data = await response.json();

        const user = data.user;

        // Save globally
        window.authUser = user;
        console.log("Authenticated user:", user.role);

        // Show authenticated UI
        guestSection.style.display = "none";

        userSection.style.display = "flex";

        // ROLE-BASED UI
        if (user.role === "admin") {

            adminLink.style.display = "inline";

        } else {

            adminLink.style.display = "none";
        }

    } catch (error) {

        // Guest UI
        window.authUser = null;

        guestSection.style.display = "flex";

        userSection.style.display = "none";
    }

    // Reveal navbar after auth check
    navbarAuth.style.display = "flex";
}


// Initialize navbar
document.addEventListener(
    "DOMContentLoaded",
    initializeNavbar
);


// Logout
logoutBtn?.addEventListener(
    "click",
    async () => {

        await logout();
    }
);