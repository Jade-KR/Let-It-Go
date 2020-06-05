import api from "../../api";
// import router from "../../router";

const state = {
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
    updated_at: "",
    parts: []
  },
  reviews: [],
  myparts: [],
  recommendList: []
};

const actions = {
  async getModelDetail({ commit }, params) {
    const resp = await api.getModelDetail(params).then(res => res.data);
    commit("setModel", resp);
    commit("setReviews", resp.reviews);
  },
  async onLike({ commit }, params) {
    commit;
    const resp = await api
      .setLike(params)
      .then(res => res.data)
      .catch(err => err);
    return resp;
  },
  async reviewWrite({ commit }, params) {
    await api.reviewWrite(params).then(res => {
      res;
      commit("resetReviews");
      api.getModelDetail(params.lego_set_id).then(resp => {
        commit("setReviews", resp.data.reviews);
      });
    });
  },
  async reviewUpdate({ commit }, params) {
    commit;
    api.reviewUpdate(params).then(res => {
      res;
      commit("resetReviews");
      api.getModelDetail(params.lego_set_id).then(resp => {
        commit("setReviews", resp.data.reviews);
      });
    });
  },
  async reviewDelete({ commit }, params) {
    api.reviewDelete(params.id).then(res => {
      res;
      commit("resetReviews");
      api.getModelDetail(params.lego_set_id).then(resp => {
        commit("setReviews", resp.data.reviews);
      });
    });
  },
  async getUserPartsAll({ commit }) {
    const resp = await api
      .getUserPartsAll()
      .then(res => res.data.results)
      .catch(err => err);
    commit("setMyParts", resp);
  },
  async addMyParts({ commit }, params) {
    commit;
    const resp = await api
      .addUserParts(params)
      .then(res => res.data)
      .catch(err => err.response);
    return resp;
  },
  async getModelsByItemBased({ commit }, params) {
    const resp = await api
      .getModelsByItemBased(params)
      .then(res => res.data)
      .catch(err => err.response);
    commit("setRecommendList", resp);
  },
  async addInven({ commit }, params) {
    commit;
    const resp = await api
      .setModelToInventory(params)
      .then(res => res.data)
      .catch(err => err.response);
    return resp;
  },
  async subInven({ commit }, params) {
    commit;
    const resp = await api
      .setModelToInventory(params)
      .then(res => res.data)
      .catch(err => err.response);
    return resp;
  }
};

const mutations = {
  setModel(state, model) {
    state.model = model;
  },
  resetModel(state) {
    state.model = {
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
      updated_at: "",
      parts: []
    };
  },
  setReviews(state, reviews) {
    state.reviews = reviews;
  },
  resetReviews(state) {
    state.reviews = [];
  },
  setMyParts(state, models) {
    state.myparts = models;
  },
  resetMyParts(state) {
    state.myparts = [];
  },
  setRecommendList(state, models) {
    state.recommendList = models;
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
