import api from "../../api";
// import router from "../../router";

const state = {
  followingList: [],
  followerList: [],
  myFollowingList: [],
  userModelList: [],
  userModelPage: "1",
  likeModelList: [],
  likeModelPage: "1",
  invenModelList: [],
  invenModelPage: "1",
  stopScroll: false
};

const actions = {
  async onFollow({ commit }, params) {
    commit;
    const resp = await api
      .setFollow(params)
      .then(res => res.data)
      .catch(err => err);
    const user_id = location.pathname.slice(8);
    actions.follower(
      {
        commit
      },
      user_id
    );
    actions.following(
      {
        commit
      },
      user_id
    );
    actions.myFollowing({
      commit
    });
    return resp;
  },
  async onFollowInModal({ commit }, params) {
    commit;
    const resp = await api
      .setFollow(params)
      .then(res => res.data)
      .catch(err => err);
    return resp;
  },
  async follower({ commit }, params) {
    const resp = await api.getFollower(params).then(res => res.data.results);
    commit("setFollowerList", resp);
  },
  async following({ commit }, params) {
    const resp = await api.getFollowing(params).then(res => res.data.results);
    commit("setFollowingList", resp);
  },
  async myFollowing({ commit }) {
    const params = localStorage.getItem("pk");
    const resp = await api.getFollowing(params).then(res => res.data.results);
    commit("setMyFollowingList", resp);
  },
  async getUserInfo({ commit }, params) {
    commit;
    const resp = await api
      .getUserInfo(params.user_id)
      .then(res => res.data)
      .catch(err => err.response.status);
    return resp;
  },
  async getUserModels({ commit }, params) {
    commit;
    const append = params.append;
    const resp = await api.getUserModels(params).then(res => res.data);
    const models = resp.results.map(e => e);
    if (append) {
      commit("addUserModelList", models);
    } else {
      commit("setUserModels", models);
    }
    commit("setUserModelPage", resp.next);
  },
  async getLikeModels({ commit }, params) {
    commit;
    const append = params.append;
    const resp = await api.getUserLikeModels(params).then(res => res.data);
    const models = resp.results.map(e => e);
    if (append) {
      commit("addLikeModelList", models);
    } else {
      commit("setLikeModels", models);
    }
    commit("setLikeModelPage", resp.next);
  },
  checkModelsCnt({ commit }, params) {
    commit;
    return api.getUserModels(params);
  },
  async userModelInven({ commit }, params) {
    commit;
    const append = params.append;
    const resp = await api
      .getModelsForInven(params)
      .then(res => res.data)
      .catch(err => err.response);
    const models = resp.results.map(e => e);
    if (append) {
      commit("addInvenModelList", models);
    } else {
      commit("setInvenModels", models);
    }
    commit("setInvenModelPage", resp.next);
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
    if (url == null) {
      return (state.stopScroll = true);
    }
    state.userModelPage = new URL(url).searchParams.get("page");
  },
  addLikeModelList(state, model) {
    state.likeModelList = state.likeModelList.concat(model);
  },
  setLikeModels(state, model) {
    state.likeModelList = model.map(e => e);
  },
  setLikeModelPage(state, url) {
    if (url == null) {
      return (state.stopScroll = true);
    }
    state.likeModelPage = new URL(url).searchParams.get("page");
  },
  addInvenModelList(state, model) {
    state.invenModelList = state.invenModelList.concat(model);
  },
  setInvenModels(state, model) {
    state.invenModelList = model.map(e => e);
  },
  setInvenModelPage(state, url) {
    if (url == null) {
      return (state.stopScroll = true);
    }
    state.invenModelPage = new URL(url).searchParams.get("page");
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
