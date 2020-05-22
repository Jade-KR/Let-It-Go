import http from "./http";

const apiUrl = "/api";

const headers = {
  authorization: "jwt " + localStorage.getItem("token")
};
export default {
  register(params) {
    return http.post(`${apiUrl}/rest-auth/registration/`, params);
  },
  login(params) {
    return http.post(`${apiUrl}/login/`, params);
  },
  writeSubmit(params) {
    return http.post(`${apiUrl}/CreateLegoSet`, params, { headers });
  },
  getModels(params) {
    return http.get(`${apiUrl}/LegoSet`, { params });
  }
};
