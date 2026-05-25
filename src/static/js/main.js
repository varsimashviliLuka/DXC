// static/js/utils/api.js
let refreshRequest = null;
let authUserRequest = null;
let authUserCache = undefined;

function getCookieValue(name) {
    const cookieRow = document.cookie
        .split("; ")
        .find((row) => row.startsWith(`${name}=`));

    if (!cookieRow) {
        return null;
    }

    return decodeURIComponent(cookieRow.split("=")[1]);
}

function isUnsafeMethod(method) {
    return !["GET", "HEAD", "OPTIONS"].includes(method);
}

function shouldAttemptRefresh(url) {
    const noRefreshPaths = new Set([
        "/api/auth/login",
        "/api/auth/registration",
        "/api/auth/refresh"
    ]);

    return !noRefreshPaths.has(url);
}

function hasRefreshSession() {
    return Boolean(getCookieValue("csrf_refresh_token"));
}

function buildHeaders(options, csrfCookieName, csrfHeaderName) {
    const headers = {
        ...(options.headers || {})
    };

    const method = (options.method || "GET").toUpperCase();
    const isJsonBody = options.body !== undefined && !(options.body instanceof FormData);

    if (isJsonBody && !headers["Content-Type"]) {
        headers["Content-Type"] = "application/json";
    }

    if (isUnsafeMethod(method) && !headers[csrfHeaderName]) {
        const csrfToken = getCookieValue(csrfCookieName);
        if (csrfToken) {
            headers[csrfHeaderName] = csrfToken;
        }
    }

    return headers;
}

async function refreshAccessToken() {
    if (!refreshRequest) {
        refreshRequest = (async () => {
            const refreshResponse = await fetch("/api/auth/refresh", {
                method: "POST",
                headers: buildHeaders({ method: "POST" }, "csrf_refresh_token", "X-CSRF-REFRESH"),
                credentials: "include"
            });

            if (!refreshResponse.ok) {
                throw new Error("Session expired");
            }
        })().finally(() => {
            refreshRequest = null;
        });
    }

    return refreshRequest;
}

async function sendRequest(url, options = {}) {
    let response = await fetch(url, {
        ...options,
        headers: buildHeaders(options, "csrf_access_token", "X-CSRF-ACCESS"),
        credentials: "include"
    });

    // Access token expired -> refresh using refresh cookie + CSRF header.
    if (
        response.status === 401 &&
        shouldAttemptRefresh(url) &&
        hasRefreshSession()
    ) {
        await refreshAccessToken();

        response = await fetch(url, {
            ...options,
            headers: buildHeaders(options, "csrf_access_token", "X-CSRF-ACCESS"),
            credentials: "include"
        });
    }

    return response;
}

async function getCurrentUser(forceReload = false) {
    if (!forceReload) {
        if (authUserCache !== undefined) {
            return authUserCache;
        }

        if (authUserRequest) {
            return authUserRequest;
        }
    }

    authUserRequest = (async () => {
        try {
            const response = await sendRequest(
                "/api/user/myuser",
                {
                    method: "GET"
                }
            );

            if (!response.ok) {
                authUserCache = null;
                return null;
            }

            const data = await response.json();
            authUserCache = data.user || null;

            return authUserCache;
        } catch (error) {
            authUserCache = null;
            return null;
        } finally {
            authUserRequest = null;
        }
    })();

    return authUserRequest;
}

function clearAuthUserCache() {
    authUserCache = undefined;
    authUserRequest = null;
}

async function isAuthenticated() {
    try {
        const user = await getCurrentUser();
        return Boolean(user);
    } catch (error) {
        console.error("Error checking authentication status:", error);
        return false;
    }
}

async function isUserAdmin() {
    try {
        const user = await getCurrentUser();
        return user?.role === "admin";
    } catch (error) {
        console.error("Error checking admin status:", error);
        return false;
    }
}
