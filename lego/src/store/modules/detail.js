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
  }
};

const actions = {
  async getModelDetail({ commit }, params) {
    commit;
    // console.log(params);
    const resp = await api.getModelDetail(params).then(res => res.data);
    // console.log(resp);
    state.model = resp;
    // console.log(state.model);
  }
};

const mutations = {};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
