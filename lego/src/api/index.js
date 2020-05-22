import http from "./http"

const apiUrl = "/api";
export default {
  register(params) {
    return http.post(`${apiUrl}/rest-auth/registration/`, params);
  },
  login(params) {
    return http.post(`${apiUrl}/login/`, params);
  },
  getUserParts() {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.get(`${apiUrl}/UserPart?page=1&page_size=21`, {
      headers
    })
  },
  addUserParts(params) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    console.log(params)
    return http.post(`${apiUrl}/UpdateUserPart`, params, {
      headers
    })
  }
};