import LegoThemes from "../../../jsonData/LegoThemes.json";

import api from "../../api";

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
    updated_at: ""
  },
  modelList: [],
  modelPage: "1",
  themes: LegoThemes["rows"],
  endPoint: false,
  searchWordByDetail: "",
  searchCateByDetail: "",
  searchByDetailFlag: false
};

const actions = {
  async getModels({ commit }, params) {
    const append = params.append;
    const resp = await api.searchModels(params).then(res => res.data);
    if (resp.count === 0) {
      return false;
    }
    const models = resp.results.map(e => e);
    if (append) {
      commit("addModelList", models);
    } else {
      commit("setModels", models);
    }
    await commit("setModelPage", resp.next);
  },
  searchByDetail({ commit }, params) {
    commit("setSearchWordByDetail", params["word"]);
    commit("setSearchCateByDetail", params["type"]);
    commit("setSearchByDetailFlag");
  }
};

const mutations = {
  setModels(state, model) {
    state.modelList = model.map(e => e);
  },
  addModelList(state, model) {
    state.modelList = state.modelList.concat(model);
  },
  setModelPage(state, url) {
    if (url === null) {
      state.endPoint = true;
      return;
    }
    state.modelPage = new URL(url).searchParams.get("page");
  },
  resetEndPoint(state) {
    state.endPoint = false;
  },
  resetModelList(state) {
    state.modelList = [];
  },
  setSearchWordByDetail(state, word) {
    state.searchWordByDetail = word;
  },
  setSearchCateByDetail(state, cate) {
    state.searchCateByDetail = cate;
  },
  setSearchByDetailFlag(state) {
    state.searchByDetailFlag = true;
  },
  resetSearchByDetailFlag(state) {
    state.searchByDetailFlag = false;
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
