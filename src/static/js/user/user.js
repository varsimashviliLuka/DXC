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
        const user = await getCurrentUser();

        if (!user) {
            window.location.href = "/";
            return;
        }

        const userPanelContainer = document.getElementById("user-panel-container");
        userPanelContainer.style.display = "block";

        populateUserInfo(user);
        await loadTransactions();
    }
);


// LOAD USER INFO
function populateUserInfo(user) {
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

            const operation = document.createElement("p");
            operation.textContent = `Operation: ${transaction.operator}`;

            const amount = document.createElement("p");
            amount.textContent = `Amount: ${transaction.amount}`;

            const timestamp = document.createElement("p");
            timestamp.textContent = `Date: ${transaction.timestamp}`;

            const separator = document.createElement("hr");

            transactionCard.appendChild(operation);
            transactionCard.appendChild(amount);
            transactionCard.appendChild(timestamp);
            transactionCard.appendChild(separator);

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