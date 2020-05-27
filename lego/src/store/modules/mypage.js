import api from "../../api";
// import router from "../../router";

const state = {
  myModels: []
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
  async getModels({
    commit
  }, params) {
    let tmp = []
    await api.getMyModels(params).then(res => {
      res.data.lego_sets.forEach(item => {
        tmp.push(item)
      })
    })
    commit("setMyModels", tmp)
  }
};

const mutations = {
  setMyModels(state, params) {
    state.myModels = params
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};