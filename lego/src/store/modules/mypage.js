import api from "../../api";
// import router from "../../router";

const state = {};

const actions = {
  async onFollow({ commit }, params) {
    commit;
    const resp = await api
      .setFollow(params)
      .then(res => res.data)
      .catch(err => err);
    return resp;
  }
};

const mutations = {};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
