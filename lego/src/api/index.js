import http from "./http";

const apiUrl = "/api";

const headers = {
  Authorization: "jwt " + localStorage.getItem("token")
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
    return http.get(`${apiUrl}/LegoSet/${params}`, {
      headers
    });
  },
  getUserParts(page) {
    return http.get(`${apiUrl}/UserPart?page=${page}&page_size=21`, {
      headers
    });
  },
  addUserParts(params) {
    return http.post(`${apiUrl}/UpdateUserPart`, params, {
      headers
    });
  },
  setLike(params) {
    return http.post(`${apiUrl}/like_set`, params, {
      headers
    });
  },
  setFollow(params) {
    return http.post(`${apiUrl}/follow`, params, {
      headers
    });
  },
  changePasssword(params) {
    return http.post(`${apiUrl}/rest-auth/password/change/`, params, {
      headers
    });
  },
  logout() {
    return http.post(`${apiUrl}/rest-auth/logout/`, {
      headers
    });
  },
  tokenVerify(params) {
    return http.post(`${apiUrl}/token/verify/`, params);
  },
  getFollower() {
    return http.get(`${apiUrl}/Follower`, { headers });
  },
  getFollowing() {
    return http.get(`${apiUrl}/Following`, { headers });
  }
};
