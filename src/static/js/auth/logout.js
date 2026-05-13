async function logout() {

    try {

        await sendRequest("/api/auth/logout", {
            method: "POST"
        });

    } catch (e) {
        console.error(e);
    }

    // Always clear frontend state
    localStorage.removeItem("access_token");

    // redirect to login page
    window.location.href = "/login";
}
