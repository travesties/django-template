import "./App.css";
import { LoginForm } from "./LoginForm";
import { UserContext } from "./UserContext";
import { useState, useCallback, useEffect, useMemo } from "react";
import { User } from "./User.jsx";
import { useVisibilityChange, useApiPolling } from "./hooks.js";
import { userLogout } from "./api.js";
import environment from "./environment.js";

function storeUserData({ user, token, expiry }) {
  localStorage.setItem("user", JSON.stringify(user));
  localStorage.setItem("token", token);
  localStorage.setItem("expiry", expiry);
}

function clearUserData() {
  localStorage.removeItem("user");
  localStorage.removeItem("token");
  localStorage.removeItem("expiry");
}

/*
 * Stores logged-in user data in localStorage and
 * updates the user data state.
 * @param {object} user - User data object
 * @param {string} token - User authentication token
 * @param {string} expiry - Auth token expiration timestamp
 */
function loginUser({ user, token, expiry }, setUser) {
  storeUserData({ user, token, expiry });
  setUser(user);
}

/*
 * Logs out the user at the API level, and then clears
 * stored user data.
 * @param {Function} setUser - user data set state method
 * @param {string} token - user authentication token
 */
function logoutUser(setUser, token) {
  userLogout(token)
    .then(() => {
      clearUserData();
      setUser(null);
    })
    .catch((error) => {
      console.log("Failed to logout", error);
    });
}

/*
 * Retrieve's the user data object from localStorage.
 * @returns {object} User data
 */
function getUser() {
  return JSON.parse(localStorage.getItem("user"));
}

/**
 * Retrieve's the user's auth token from localStorage. If the
 * token is expired, the user and token data entries in
 * localStorage are deleted so that the login page is rendered.
 * @returns {string} User authentication token
 */
function getAuthToken() {
  const token = localStorage.getItem("token");
  const expiry = Date.parse(localStorage.getItem("expiry"));

  if (!token || !expiry || expiry < Date.now()) {
    clearUserData();
    return null;
  }

  return token;
}

function App() {
  const documentVisible = useVisibilityChange();
  const [initialLoadInProgress, setInitialLoadInProgress] = useState(false);
  const [initialLoadComplete, setInitialLoadComplete] = useState(false);
  const [isPageVisible, setIsPageVisible] = useState(true);
  const [token, setToken] = useState(getAuthToken());
  const [user, setUser] = useState(getUser());

  function handleUnauthorizedUser(response) {
    if (response.status === 401) {
      clearUserData();
      setUser(null);
      setInitialLoadInProgress(false);
      setInitialLoadComplete(false);
      throw new Error("Unauthorized. Reset client credentials.");
    }
    return response;
  }

  // Perform immediate watchlist load when user logs in.
  if (user && !initialLoadComplete && !initialLoadInProgress) {
    // Perform initial data load
    setInitialLoadComplete(true);
    setInitialLoadInProgress(false);
  }

  // Poll watchlist endpoint on 5 second interval.
  //const watchlistPoll = useApiPolling(() => {
  //  if (!user || !initialLoadComplete || !marketIsOpen || !isPageVisible || watchlist.length === 0) {
  //    return null;
  //  }
  //  return getWatchlist(token).then((res) => {
  //    return handleUnauthorizedUser(res);
  //  });
  //}, environment.WATCHLIST_REFRESH_INTERVAL);

  //if (watchlistPoll && watchlistPoll.ok && !watchlistPoll.bodyUsed) {
  //  watchlistPoll.json()
  //  .then((data) => {
  //    data.trackers.forEach(t => t.security.last_modified = new Date(t.security.last_modified));
  //    setWatchlist(data.trackers);
  //  })
  //  .catch((error) => {
  //    console.log('Failed to load watchlist:', error.message);
  //  });
  //}

  // There is no reason to request watchlist price updates if the document is
  // no longer visible. We subscribe to the document's visibilityState property
  // so that we may halt price update requests when the user is not viewing
  // the application.
  useEffect(() => {
    setIsPageVisible(documentVisible);
  }, [documentVisible]);

  const login = useCallback((data) => {
    // TODO: handle login failure
    storeUserData(data);
    setUser(data.user);
    setToken(data.token);
  });

  const logout = useCallback(() => logoutUser(setUser, token), [token]);
  const value = useMemo(
    () => ({ user, token, login, logout }),
    [user, token, login, logout],
  );

  return (
    <UserContext.Provider value={value}>
      <div className="app">
        <LoginForm />
        <header>
          <h1>Example App</h1>
          <User />
        </header>
        {user && (
          <section>
            <p>Hello, world!</p>
          </section>
        )}
      </div>
    </UserContext.Provider>
  );
}

export default App;
