import api from "../../api";

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
  modelPage: "1",
  likeModelPage: "1",
  recommendModelPage: "1",
  modelAllCnt: 0,
  likeModelAllCnt: 0,
  recommendModelAllCnt: 0
};

const actions = {
  async getModels({ commit }, params) {
    const append = params.append;
    const resp = await api.getModels(params).then(res => res.data);
    if (state.modelAllCnt === 0) {
      commit("setModelAllCnt", resp.count);
    }
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
    if (state.likeModelAllCnt === 0) {
      commit("setLikeModelAllCnt", resp.count);
    }
    const models = resp.results.map(e => e);
    if (append) {
      commit("addModelList", models);
    } else {
      commit("setModels", models);
    }
    commit("setLikeModelPage", resp.next);
  },
  async getRecommendModels({ commit }, params) {
    var append = params.append;
    const resp = await api.getModelsByUserBased(params).then(res => res.data);
    if (state.recommendModelAllCnt === 0) {
      commit("setRecommendModelAllCnt", resp.count);
    }
    const models = resp.results.map(e => e);
    if (append) {
      commit("addModelList", models);
    } else {
      commit("setModels", models);
    }
    commit("setRecommendModelPage", resp.next);
  },
  async setUserCategory({ commit }, params) {
    commit;
    const resp = await api
      .setUserCategory(params)
      .then(res => res.data)
      .catch(err => err.response);
    if (resp === "카테고리 등록 완료") {
      localStorage.setItem("categories", params["categories"]);
    }
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
    if (url !== null) {
      state.modelPage = new URL(url).searchParams.get("page");
    } else {
      state.modelPage = String(Number(state.modelPage) + 1);
    }
  },
  setModelAllCnt(state, cnt) {
    state.modelAllCnt = Math.ceil(cnt / 10) === 1 ? 2 : Math.ceil(cnt / 10);
  },
  setLikeModelPage(state, url) {
    if (url !== null) {
      state.likeModelPage = new URL(url).searchParams.get("page");
    } else {
      state.likeModelPage = String(Number(state.likeModelPage) + 1);
    }
  },
  setLikeModelAllCnt(state, cnt) {
    state.likeModelAllCnt = Math.ceil(cnt / 10) === 1 ? 2 : Math.ceil(cnt / 10);
  },
  setRecommendModelPage(state, url) {
    if (url !== null) {
      state.recommendModelPage = new URL(url).searchParams.get("page");
    } else {
      state.recommendModelPage = String(Number(state.recommendModelPage) + 1);
    }
  },
  setRecommendModelAllCnt(state, cnt) {
    state.recommendModelAllCnt =
      Math.ceil(cnt / 10) === 1 ? 2 : Math.ceil(cnt / 10);
  },
  resetModels(state) {
    state.modelList = [];
    state.modelPage = "1";
    state.likeModelPage = "1";
  },
  resetPages(state) {
    state.modelPage = "1";
    state.likeModelPage = "1";
    state.recommendModelPage = "1";
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
