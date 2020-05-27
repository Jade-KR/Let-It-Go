import api from "../../api";
// import router from "../../router";

const state = {
  followingList: [],
  followerList: [],
  myFollowingList: [],
  userModelList: [],
  userModelPage: "1"
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
  async follower({
    commit
  }, params) {
    const resp = await api.getFollower(params).then(res => res.data.results);
    commit("setFollowerList", resp);
  },
  async following({
    commit
  }, params) {
    const resp = await api.getFollowing(params).then(res => res.data.results);
    commit("setFollowingList", resp);
  },
  async myFollowing({
    commit
  }) {
    const params = localStorage.getItem("pk");
    const resp = await api.getFollowing(params).then(res => res.data.results);
    commit("setMyFollowingList", resp);
  },
  async getUserInfo({
    commit
  }, params) {
    commit;
    const resp = await api
      .getUserInfo(params.user_id)
      .then(res => res.data)
      .catch(err => err.response.status);
    return resp;
  },
  async getUserModels({
    commit
  }, params) {
    commit;
    const append = params.append;
    const resp = await api.getUserModels(params).then(res => res.data);
    const models = resp.results.map(e => e);
    console.log(models)
    if (append) {
      commit("addUserModelList", models);
    } else {
      commit("setUserModels", models);
    }
    commit("setUserModelPage", resp.next);
  }
};

const mutations = {
  setFollowingList(state, followings) {
    state.followingList = followings.map(s => s);
  },
  setFollowerList(state, followers) {
    state.followerList = followers.map(s => s);
  },
  setMyFollowingList(state, followings) {
    state.myFollowingList = followings.map(s => s);
  },
  addUserModelList(state, model) {
    state.userModelList = state.userModelList.concat(model);
  },
  setUserModels(state, model) {
    state.userModelList = model.map(e => e);
  },
  setUserModelPage(state, url) {
    console.log(url)
    state.userModelPage = url
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};