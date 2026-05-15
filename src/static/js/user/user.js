const userEmail =
    document.getElementById("userEmail");

const userPhone =
    document.getElementById("userPhone");

const userPersonalNumber =
    document.getElementById("userPersonalNumber");

const userBalance =
    document.getElementById("userBalance");

const userStatus =
    document.getElementById("userStatus");

const transactionsList =
    document.getElementById("transactionsList");


// PAGE INIT
document.addEventListener(
    "DOMContentLoaded",
    async () => {

        const loggedIn = await isAuthenticated();

     if (!loggedIn) {

        // User already logged in
        window.location.href = "/";
    }else{
        userPanelContainer = document.getElementById("user-panel-container");
        userPanelContainer.style.display = "block";

        await loadUser();

        await loadTransactions();
    }}
);


// LOAD USER INFO
async function loadUser() {

    try {

        const response = await sendRequest(
            "/api/user/myuser",
            {
                method: "GET"
            }
        );

        const data = await response.json();

        console.log("User:", data);

        if (!response.ok) {

            throw new Error(
                data.error || "Failed to load user."
            );
        }

        const user = data.user;

        userEmail.textContent =
            user.email;

        userPhone.textContent =
            user.phone_number;

        userPersonalNumber.textContent =
            user.personal_number;

        userBalance.textContent =
            user.balance;

        userStatus.textContent =
            user.active
                ? "Active"
                : "Inactive";

    } catch (error) {

        console.error(error);
    }
}


// LOAD TRANSACTIONS
async function loadTransactions() {

    try {

        const response = await sendRequest(
            "/api/user/myuser/transactions",
            {
                method: "GET"
            }
        );

        const data = await response.json();

        console.log("Transactions:", data);

        transactionsList.innerHTML = "";

        if (!response.ok) {

            transactionsList.innerHTML = `
                <p>
                    No transactions found.
                </p>
            `;

            return;
        }

        data.transactions.forEach(transaction => {

            const transactionCard =
                document.createElement("div");

            transactionCard.classList.add(
                "transaction-card"
            );

            transactionCard.innerHTML = `

                <p>
                    <strong>Operation:</strong>
                    ${transaction.operator}
                </p>

                <p>
                    <strong>Amount:</strong>
                    ${transaction.amount}
                </p>

                <p>
                    <strong>Date:</strong>
                    ${transaction.timestamp}
                </p>

                <hr>
            `;

            transactionsList.appendChild(
                transactionCard
            );
        });

    } catch (error) {

        console.error(error);

        transactionsList.innerHTML = `
            <p>
                Failed to load transactions.
            </p>
        `;
    }
}