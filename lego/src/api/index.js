import http from "./http";

const apiUrl = "/api";

const token = localStorage.getItem("token");
const headers = {
  Authorization: token !== null ? "jwt " + token : null
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
      params,
      headers
    });
  },
  getLikeModels(params) {
    return http.get(`${apiUrl}/LegoSetRanking`, {
      params,
      headers
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
  getFollower(params) {
    return http.get(`${apiUrl}/Follower/${params}`, {
      headers
    });
  },
  getFollowing(params) {
    return http.get(`${apiUrl}/Following/${params}`, {
      headers
    });
  },
  getUserInfo(params) {
    return http.get(`${apiUrl}/User/${params}`);
  },
  searchModels(params) {
    return http.get(`${apiUrl}/LegoSet`, {
      params,
      headers
    });
  },
  reviewWrite(params) {
    return http.post(`${apiUrl}/Review`, params, {
      headers
    });
  },
  reviewUpdate(params) {
    return http.put(`${apiUrl}/Review/${params.id}`, params.info, { headers });
  },
  reviewDelete(params) {
    return http.delete(`${apiUrl}/Review/${params}`, {
      headers
    });
  },
  getUserModels(params) {
    return http.get(`${apiUrl}/UserLegoSet/${params.id}?page_size=12`, {
      params
    });
  },
  changProfilePic(params) {
    return http.put(`${apiUrl}/UpdateUserProfile`, params, {
      headers
    });
  },
  updateUserInfo(params) {
    const info = {
      nickname: params.nickname,
      email: params.email,
      comment: params.comment
    };
    return http.put(`${apiUrl}/User/${params.id}`, info, {
      headers
    });
  },
  getUserLikeModels(params) {
    return http.get(`${apiUrl}/UserLikeLegoSet/${params.id}?page_size=12`, {
      params
    });
  }
};
