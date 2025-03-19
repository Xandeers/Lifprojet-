// import axios from "axios";

// const API = axios.create({
//   baseURL: "http://127.0.0.1:5000",
//   withCredentials: true,
// });

const baseURL = "http://127.0.0.1:5000";

const fetchAPI = (
  method: "GET" | "POST" | "PUT" | "DELETE",
  endpoint: string,
  data?: Object
) => {
  return fetch(baseURL + endpoint, {
    method,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(data),
  });
};

export default fetchAPI;
