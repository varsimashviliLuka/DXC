const getUserButton =
    document.getElementById("getUserButton");

const userData =
    document.getElementById("userData");

getUserButton.addEventListener("click", async () => {

    try {

        const response = await sendRequest(
            "/api/user/myuser",
            {
                method: "GET"
            }
        );

        const data = await response.json();

        console.log(data);

        if (response.ok) {

            userData.textContent =
                JSON.stringify(data, null, 4);

        } else {

            userData.textContent =
                data.error || "Failed to fetch user.";
        }

    } catch (error) {

        console.error(error);

        userData.textContent =
            "Something went wrong.";

        window.location.href = "/login";
    }
});