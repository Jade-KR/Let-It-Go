import LegoParts from "../../../jsonData/LegoParts.json";
import LegoCategory from "../../../jsonData/LegoCategory.json";


const state = {
  legoParts: LegoParts,
  legoCategory: LegoCategory,
  filtered: [],
  currentStep: 0,
  pickedPart: ''
}

const mutations = {
  setCurrentStep(state, step) {
    state.currentStep = step
  },
  setFiltered(state, result) {
    state.filtered = result
  },
  setPart(state, id) {
    state.pickedPart = id
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
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
};