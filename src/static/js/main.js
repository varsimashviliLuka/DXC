// static/js/utils/api.js

async function sendRequest(url, options = {}) {

    // Get stored access token
    let accessToken = localStorage.getItem("access_token");

    // Default headers
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    // Add Authorization header if token exists
    if (accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }

    // First request
    let response = await fetch(url, {
        ...options,
        headers,
        credentials: "include"
    });

    // If access token expired -> try refresh
    if (response.status === 401) {

        const refreshResponse = await fetch("/api/auth/refresh", {
            method: "POST",
            credentials: "include"
        });

        // Refresh failed -> logout user
        if (!refreshResponse.ok) {

            localStorage.removeItem("access_token");


            throw new Error("Session expired");
        }

        // Save new access token
        const refreshData = await refreshResponse.json();

        localStorage.setItem(
            "access_token",
            refreshData.access_token
        );

        accessToken = refreshData.access_token;

        // Retry original request
        const retryHeaders = {
            ...headers,
            Authorization: `Bearer ${accessToken}`
        };

        response = await fetch(url, {
            ...options,
            headers: retryHeaders,
            credentials: "include"
        });
    }

    return response;
}

async function isAuthenticated() {
    try {
        const response = await sendRequest(
            "/api/auth/check"
        );

        return response.ok;
    } catch (error) {
        console.error("Error checking authentication status:", error);
        return false;
    }
}
