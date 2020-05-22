import LegoParts from "../../../jsonData/LegoParts.json";
import LegoCategory from "../../../jsonData/LegoCategory.json";
import LegoColor from "../../../jsonData/LegoColors.json"
import api from "../../api";


const state = {
  legoParts: LegoParts,
  legoCategory: LegoCategory,
  filtered: [],
  currentStep: 0,
  pickedPart: '',
  legoColor: LegoColor.rows,
  basket: [],
  userParts: []
}

const mutations = {
  setCurrentStep(state, step) {
    if (step === "start") {
      state.currentStep = 0
    } else if (step === "back") {
      state.currentStep -= 1
    } else if (step === "next") {
      state.currentStep += 1
    }
  },
  setFiltered(state, result) {
    state.filtered = result
  },
  setPart(state, id) {
    state.pickedPart = id
  },
  setBasket(state, info) {
    let check = 0
    if (state.basket.length === 0) {
      state.basket.push(info)
    } else {
      state.basket.forEach(item => {
        if (item.colorId === info.colorId && item.partId === info.partId) {
          item.quantity += info.quantity
          check = 1
          return
        }
      })
      if (check === 0) {
        state.basket.push(info)
      }
    }

  },
  takeOutBasket(state, idx) {
    state.basket.splice(idx, 1)
  },
  resetBasket(state) {
    state.basket = []
  },
  setUserParts(state, params) {
    state.userParts = params
  }
}


const actions = {
  legoFilter({
    commit
  }, params) {
    let filteredParts = LegoParts.rows.filter(part => {
      return part[5] === params
    });
    commit("setFiltered", filteredParts)
  },
  changeStep({
    commit
  }, params) {
    commit("setCurrentStep", params)
  },
  pickPart({
    commit
  }, params) {
    commit("setPart", params)
  },
  addBasket({
    commit
  }, params) {
    commit("setBasket", params)
  },
  deleteBasket({
    commit
  }, params) {
    commit("takeOutBasket", params)
  },
  async updateParts({
    commit
  }, params) {
    await api.addUserParts(params)
    commit("resetBasket")
  },
  async getUserParts({
    commit
  }) {
    const resp = await api.getUserParts()
    console.log(resp)
    console.log(resp)
    commit("setUserParts", resp.data.results)
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
};