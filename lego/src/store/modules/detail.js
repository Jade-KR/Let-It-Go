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
    commit;
    console.log("getmodel params", params);
    const resp = await api.getModelDetail(params).then(res => res.data);
    state.model = resp;
    state.reviews = resp.reviews;
    console.log(state.model);
    console.log(state.reviews);
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
    commit;
    console.log(params);
    await api.reviewWrite(params).then(res => {
      res;
      api.getModelDetail(params.lego_set_id).then(resp => {
        console.log(resp.data.reviews);
        state.reviews = resp.data.reviews;
      });
    });
  }
};

const mutations = {
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
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
