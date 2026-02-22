(function () {
    var visitorId = "ddb_vid";
    var sessionId = "ddb_sid";

    var extendSessionCookie = function () {
        var session = getCookie(sessionId);
        if (session) {
            setCookie(sessionId, session, {
                "max-age": 60 * 60 * 4, // 4 hours
                secure: true,
                SameSite: "Lax"
            });
        }
    }

    var getCookie = function (name) {
        var cookieName = name + "=([^;]*)";
        var cookie = document.cookie.match(cookieName);
        if (cookie) {
            return cookie[1];
        }

        return;
    }

    var setCookie = function (name, value, opts) {
        var cookieNameValue = name + "=" + value;
        var maxage = "max-age=" + opts["max-age"];
        var sameSite = "SameSite=" + opts["SameSite"];
        var parts = [cookieNameValue, maxage, sameSite];
        if (opts.secure) {
            parts.push("secure", "domain=.dndbeyond.com", "path=/");
        }
        return (document.cookie = parts.join(";"));
    };

    var deleteCookie = function (name) {
        setCookie(name, "", { "max-age": 0, secure: true });
    }

    var createSessionAndVisitorCookies = function () {
        if (!getCookie(visitorId)) {
            setCookie(visitorId, crypto.randomUUID(), {
                "max-age": 60 * 60 * 24 * 365, // 1 year
                secure: true,
                SameSite: "Lax"
            });
        }
        if (!getCookie(sessionId)) {
            setCookie(sessionId, crypto.randomUUID(), {
                "max-age": 60 * 60 * 4, // 4 hours
                secure: true,
                SameSite: "Lax"
            })
        } else {
            extendSessionCookie();
        }
    }

    var initialize = function () {
        var maxRetries = 10;
        var retryInterval = 500;
        var retries = 0;
        var tryInitialize = function () {
            if ("window" in globalThis && window.ketch) {
                window.ketch("on", "consent", function (consentData) {
                    if (!consentData.purposes.analytics) {
                        deleteCookie(visitorId);
                        deleteCookie(sessionId);
                    } else {
                        createSessionAndVisitorCookies();
                    }
                });
            } else if (retries < maxRetries) {
                retries++;
                setTimeout(tryInitialize, retryInterval);
            } else {
                console.warn("Failed to initialize session cookies.");
            }
        };

        tryInitialize();
    }

    initialize();
})();
