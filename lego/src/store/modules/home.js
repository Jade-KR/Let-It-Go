import api from "../../api";
// import router from "../../router";

const state = {
  homeCate: 1,
  model: {
    id: 0,
    images: "",
    name: "",
    num_part: 0,
    description: "",
    tags: "",
    references: "",
    theme_id: 0,
    user_id: 0,
    created_at: "",
    updated_at: ""
  },
  modelList: [],
  modelPage: "1"
};

const actions = {
  async getModels({ commit }, params) {
    const append = params.append;
    const resp = await api.getModels(params).then(res => res.data);
    const models = resp.results.map(e => e);
    if (append) {
      commit("addModelList", models);
    } else {
      commit("setModels", models);
    }
    commit("setModelPage", resp.next);
  },
  async onLike({ commit }, params) {
    commit;
    const resp = await api
      .setLike(params)
      .then(res => res.data)
      .catch(err => err);
    return resp;
  },
  async getLikeModels({ commit }, params) {
    const append = params.append;
    const resp = await api.getLikeModels(params).then(res => res.data);
    const models = resp.results.map(e => e);
    console.log(models);
    if (append) {
      commit("addModelList", models);
    } else {
      commit("setModels", models);
    }
    commit("setModelPage", resp.next);
  }
};

const mutations = {
  setHomeCate(state, value) {
    state.homeCate = value;
  },
  setModels(state, model) {
    state.modelList = model.map(e => e);
  },
  addModelList(state, model) {
    state.modelList = state.modelList.concat(model);
  },
  setModelPage(state, url) {
    state.modelPage = new URL(url).searchParams.get("page");
  },
  resetModels(state) {
    state.modelList = [];
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
