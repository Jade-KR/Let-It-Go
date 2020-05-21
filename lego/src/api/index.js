import http from "./http";

const apiUrl = "/api";
export default {
  register(params) {
    console.log(params);
    return http.post(`${apiUrl}/rest-auth/registration/`, params);
  }
};
