import api from "../../api";
// import router from "../../router";

const state = {
  followingList: [],
  followerList: []
};

const actions = {
  async onFollow({
    commit
  }, params) {
    commit;
    const resp = await api
      .setFollow(params)
      .then(res => res.data)
      .catch(err => err);
    return resp;
  },
  async follower({ commit }) {
    commit;
    const resp = await api.getFollower().then(res => res.data.results);
    commit("setFollowerList", resp);
  },
  async following({ commit }) {
    commit;
    const resp = await api.getFollowing().then(res => res.data.results);
    commit("setFollowingList", resp);
  },
  async getUserInfo({ commit }, params) {
    commit;
    const resp = await api
      .getUserInfo(params.user_id)
      .then(res => res.data)
      .catch(err => err.response.status);
    return resp;
  }
};

const mutations = {
  setFollowingList(state, followings) {
    state.followingList = followings.map(s => s);
  },
  setFollowerList(state, followers) {
    state.followerList = followers.map(s => s);
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};