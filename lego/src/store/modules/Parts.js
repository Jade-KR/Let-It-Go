import LegoParts from "../../../jsonData/LegoParts.json";
import LegoCategory from "../../../jsonData/LegoCategory.json";
import LegoColor from "../../../jsonData/LegoColors.json";
import api from "../../api";

const state = {
  legoParts: LegoParts,
  legoCategory: LegoCategory,
  filtered: [],
  currentStep: 0,
  pickedPart: [],
  legoColor: LegoColor.rows,
  basket: [],
  userParts: [],
  partPageLength: 1,
  originalCnt: 0,
  stopScroll: false,
  partList: [],
  partPage: "1",
  userAllParts: []
};

const mutations = {
  setCurrentStep(state, step) {
    if (step === "start") {
      state.currentStep = 0;
    } else if (step === "back") {
      state.currentStep -= 1;
    } else if (step === "next") {
      state.currentStep += 1;
    }
  },
  setFiltered(state, result) {
    state.filtered = result;
  },
  setPart(state, id) {
    state.pickedPart.push(id);
  },
  resetPart(state) {
    state.pickedPart = [];
  },
  setBasket(state, info) {
    let check = 0;
    if (state.basket.length === 0) {
      state.basket.push(info);
    } else {
      state.basket.forEach(item => {
        if (item.colorId === info.colorId && item.partId === info.partId) {
          item.quantity += info.quantity;
          check = 1;
          return;
        }
      });
      if (check === 0) {
        state.basket.push(info);
      }
    }
  },
  takeOutBasket(state, idx) {
    state.basket.splice(idx, 1);
  },
  resetBasket(state) {
    state.basket = [];
  },
  setUserParts(state, params) {
    state.userParts = params.results;
    state.partPageLength = Math.ceil(params.count / 21);
  },
  deleteAllParts(state) {
    state.userParts = new Array();
  },
  setParts(state, model) {
    state.partList = model.map(e => e);
  },
  setPartPage(state, url) {
    if (url == null) {
      return (state.stopScroll = true);
    }
    state.partPage = new URL(url).searchParams.get("page");
  },
  addPartList(state, model) {
    state.partList = state.partList.concat(model);
  },
  setUserPartsAll(state, parts) {
    state.userAllParts = parts;
  }
};

const actions = {
  legoFilter({ commit }, params) {
    let filteredParts = LegoParts.rows.filter(part => {
      return part[5] === params;
    });
    commit("setFiltered", filteredParts);
  },
  changeStep({ commit }, params) {
    commit("setCurrentStep", params);
  },
  pickPart({ commit }, params) {
    if (params["isHave"] === true) {
      const temp = [];
      for (let i = 0; i < state.pickedPart.length; ++i) {
        if (state.pickedPart[i] === params["id"]) {
          continue;
        }
        temp.push(state.pickedPart[i]);
      }
      commit("resetPart");
      for (let i = 0; i < temp.length; ++i) {
        commit("setPart", temp[i]);
      }
      return;
    }
    commit("setPart", params["id"]);
  },
  addBasket({ commit }, params) {
    commit("setBasket", params);
  },
  deleteBasket({ commit }, params) {
    commit("takeOutBasket", params);
  },
  async updateParts({ commit }, params) {
    await api.addUserParts(params).then(res => {
      res;
      api.getUserPartsAll().then(res => {
        commit("setUserPartsAll", res.data.results);
      });
    });
    commit("resetBasket");
  },
  async resetLegoRail({commit}, params) {
      commit;
      params;
      await api.resetLegoRail()
  },
  async getUserParts({ commit }, page) {
    const resp = await api.getUserParts(page);
    commit("setUserParts", resp.data);
  },
  async deleteAll({ commit }) {
    commit("deleteAllParts");
  },
  async getParts({ commit }, params) {
    commit;
    const append = params.append;
    const resp = await api.getUserParts(params).then(res => res.data);
    const models = resp.results.map(e => e);
    if (append) {
      commit("addPartList", models);
    } else {
      commit("setParts", models);
    }
    commit("setPartPage", resp.next);
  },
  resetStop() {
    state.stopScroll = false;
  },
  async getAllParts({ commit }) {
    commit;
    const resp = await api
      .getUserPartsAll()
      .then(res => res.data)
      .catch(err => err.response);
    commit("setUserPartsAll", resp.results);
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
