async function logout() {

    try {

        await sendRequest("/api/auth/logout", {
            method: "POST"
        });

    } catch (e) {
        console.error(e);
    }

    // redirect to login page
    window.location.reload();
}
