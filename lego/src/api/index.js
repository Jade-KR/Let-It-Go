import http from "./http"

const apiUrl = "/api";
export default {
  register(params) {
    return http.post(`${apiUrl}/rest-auth/registration/`, params);
  },
  login(params) {
    return http.post(`${apiUrl}/login/`, params);
  }
};