import LegoParts from "../../../jsonData/LegoParts.json";
import LegoCategory from "../../../jsonData/LegoCategory.json";
import LegoColor from "../../../jsonData/LegoColors.json"


const state = {
  legoParts: LegoParts,
  legoCategory: LegoCategory,
  filtered: [],
  currentStep: 0,
  pickedPart: '',
  legoColor: LegoColor.rows,
  basket: []
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
  },
  setBasket(state, info) {
    state.basket.push(info)
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
    let info = {
      img: '',
      id: params.id,
      quantity: params.quantity
    };
    console.log(info)
    for (let i = 0; i < LegoParts.rows.length; i++) {
      if (LegoParts.rows[i][0] === info.id) {
        info.img = LegoParts.rows[i][2]
        break
      }
    }
    console.log(info)
    commit("setBasket", info)
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
};