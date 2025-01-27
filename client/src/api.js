import environment from "./environment.js";

const commonHeaders = {
  Accept: "application/json",
  "Content-Type": "application/json",
};

function httpGet({ path, params = {}, headers = {} }) {
  let url = environment.API_BASE_URL + path;

  if (params) {
    url += "?" + new URLSearchParams(params);
  }

  headers = { ...commonHeaders, ...headers };

  return fetch(url, {
    method: "GET",
    credentials: "include",
    headers,
  });
}

function httpPost({ path, data = {}, headers = {} }) {
  const body = data instanceof String ? data : JSON.stringify(data);
  headers = { ...commonHeaders, ...headers };

  return fetch(environment.API_BASE_URL + path, {
    method: "POST",
    credentials: "include",
    headers,
    body,
  });
}

function httpDelete({ path, headers = {} }) {
  headers = { ...commonHeaders, ...headers };

  return fetch(environment.API_BASE_URL + path, {
    method: "DELETE",
    credentials: "include",
    headers,
  });
}

/**
 * Logs in the user at the API level using basic authentication.
 * @param {string} username
 * @param {string} password
 * @returns {Promise} Login POST request
 */
export function userLogin(username, password) {
  return httpPost({
    path: "login/",
    data: { username, password },
  });
}

/**
 * Logs out the user at the API level using token authentication.
 * @param {string} token - User authentication token
 * @returns {Promise} Logout POST request
 */
export function userLogout(token) {
  return httpPost({
    path: "logout/",
    headers: { Authorization: `Token ${token}` },
  });
}

