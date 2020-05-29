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
  reviews: []
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
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
