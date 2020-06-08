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
  getUserParts(params) {
    return http.get(`${apiUrl}/UserPart?page=${params.page}&page_size=21`, {
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
    return http.put(`${apiUrl}/Review/${params.id}`, params.info, {
      headers
    });
  },
  reviewDelete(params) {
    return http.delete(`${apiUrl}/Review/${params}`, {
      headers
    });
  },
  getUserModels(params) {
    return http.get(`${apiUrl}/UserLegoSet/${params.id}?page_size=12`, {
      params,
      headers
    });
  },
  changeProfilePic(params) {
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
      params,
      headers
    });
  },
  getUserPartsAll() {
    return http.get(`${apiUrl}/UserPart?page_size=10000`, {
      headers
    });
  },
  setUserCategory(params) {
    return http.post(`${apiUrl}/set_user_category`, params, {
      headers
    });
  },
  delelteModel(params) {
    return http.delete(`${apiUrl}/LegoSet/${params}`, {
      headers
    });
  },
  getUsers(params) {
    return http.get(`${apiUrl}/User`, {
      params,
      headers
    });
  },
  delelteUser(params) {
    return http.delete(`${apiUrl}/User/${params}`, {
      headers
    });
  },
  changeUserStaff(params) {
    return http.put(
      `${apiUrl}/User/${params}`,
      {},
      {
        headers
      }
    );
  },
  getReviews(params) {
    return http.get(`${apiUrl}/Review`, {
      params,
      headers
    });
  },
  deleteReview(params) {
    return http.delete(`${apiUrl}/Review/${params}`, {
      headers
    });
  },
  getModelsByItemBased(params) {
    return http.get(`${apiUrl}/ItemBasedRecommend/${params}`, {
      headers
    });
  },
  getModelsByUserBased(params) {
    return http.get(`${apiUrl}/UserBasedRecommend`, { params, headers });
  },
  setModelToInventory(params) {
    return http.post(`${apiUrl}/update_user_set_inventory`, params, {
      headers
    });
  },
  getPartsFromLegoRail() {
    return http.get(`${apiUrl}/user_parts_registered_by_IoT`, {
      headers
    });
  },
  getModelsForInven(params) {
    return http.get(`${apiUrl}/UserSet`, { params, headers });
  },
  resetLegoRail() {
    const params = 'null'
    return http.post(`${apiUrl}/update_user_set_inventory2`, params, { headers });
  }
};
