const usersList =
    document.getElementById("usersList");

const editUserForm =
    document.getElementById("editUserForm");

const balanceForm =
    document.getElementById("balanceForm");

const message =
    document.getElementById("message");


// PAGE PROTECTION
document.addEventListener(
    "DOMContentLoaded",
    async () => {

        const isAdmin = await isUserAdmin();

        if (!isAdmin) {

            window.location.href = "/";

            return;
        }
        adminContainer = document.getElementById("admin-container");
        adminContainer.style.display = "block";
        await loadUsers();
    }
);


// LOAD ALL USERS
async function loadUsers() {

    try {

        const response = await sendRequest(
            "/api/user",
            {
                method: "GET"
            }
        );

        const data = await response.json();

        console.log(data);

        usersList.innerHTML = "";

        data.users.forEach(user => {

            const userCard =
                document.createElement("div");

            userCard.classList.add("user-card");

            userCard.innerHTML = `
                <p><strong>${user.email}</strong></p>
                <p>Balance: ${user.balance}</p>
                <p>Role: ${user.role}</p>
            `;

            userCard.addEventListener(
                "click",
                () => populateUser(user)
            );

            usersList.appendChild(userCard);
        });

    } catch (error) {

        console.error(error);
    }
}


// POPULATE FORM
function populateUser(user) {

    document.getElementById("userId").value =
        user.id;

    document.getElementById("email").value =
        user.email || "";

    document.getElementById("phone_number").value =
        user.phone_number || "";

    document.getElementById("personal_number").value =
        user.personal_number || "";

    document.getElementById("active").value =
        user.active ? "true" : "false";
}


// EDIT USER
editUserForm.addEventListener(
    "submit",
    async (e) => {

        e.preventDefault();

        const payload = {

            id:
                document.getElementById("userId").value,

            email:
                document.getElementById("email").value,

            phone_number:
                document.getElementById("phone_number").value,

            personal_number:
                document.getElementById("personal_number").value,

            active:
                document.getElementById("active").value === "true"
        };

        try {

            const response = await sendRequest(
                "/api/user",
                {
                    method: "PUT",

                    body: JSON.stringify(payload)
                }
            );

            const data = await response.json();

            console.log(data);

            if (response.ok) {

                message.textContent =
                    "User updated successfully.";

                await loadUsers();

            } else {

                message.textContent =
                    data.error || "Update failed.";
            }

        } catch (error) {

            console.error(error);

            message.textContent =
                "Something went wrong.";
        }
    }
);


// MODIFY BALANCE
balanceForm.addEventListener(
    "submit",
    async (e) => {

        e.preventDefault();

        const payload = {

            id:
                document.getElementById("userId").value,

            operator:
                document.getElementById("operator").value,

            amount:
                parseFloat(
                    document.getElementById("amount").value
                )
        };

        try {

            const response = await sendRequest(
                "/api/user",
                {
                    method: "PATCH",

                    body: JSON.stringify(payload)
                }
            );

            const data = await response.json();

            console.log(data);

            if (response.ok) {

                message.textContent =
                    "Balance updated successfully.";

                await loadUsers();

            } else {

                message.textContent =
                    data.error || "Balance update failed.";
            }

        } catch (error) {

            console.error(error);

            message.textContent =
                "Something went wrong.";
        }
    }
);