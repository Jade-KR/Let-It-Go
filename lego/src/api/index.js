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
    return http.post(`${apiUrl}/CreateLegoSet`, params, {
      headers
    });
  },
  getModels(params) {
    return http.get(`${apiUrl}/LegoSet`, {
      params
    });
  },
  getModelDetail(params) {
    return http.get(`${apiUrl}/LegoSet/${params}`);
  },
  getUserParts(page) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.get(`${apiUrl}/UserPart?page=${page}&page_size=21`, {
      headers
    })
  },
  addUserParts(params) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.post(`${apiUrl}/UpdateUserPart`, params, {
      headers
    })

  }
}