const state = {
  model: {
    theme_name: "",
    set_image: "",
    set_name: "",
    description: "",
    tags: "",
    reference: "",
    parts: {
      part_id: "",
      color_id: "",
      quantity: 0
    }
  },
  step: 1,
  currentStep: 1,
  modelImgs: [],
  imgFiles: "",
  descParams: {
    set_name: "",
    theme_name: null,
    tags: "",
    description: "",
    reference: ""
  },
  enrolledPart: []
};

const actions = {
  next({ commit }, params) {
    console.log(state.descParams);
    if (params.step === 1) {
      commit("setImage", state.modelImgs);
    } else if (params.step === 2) {
      commit("setDesc", state.descParams);
    }
    const step2 = document.getElementById("progress_step2");
    const step3 = document.getElementById("progress_step3");
    if (params.idx === 2) {
      step2.addEventListener("click", commit("setSteps", params.idx));
    } else if (params.idx === 3) {
      step3.addEventListener("click", commit("setSteps", params.idx));
    }
  },
  prev({ commit }, params) {
    console.log(state.descParams);
    if (params.step === 2) {
      commit("setDesc", state.descParams);
    }
    const step1 = document.getElementById("progress_step1");
    const step2 = document.getElementById("progress_step2");
    if (params.idx === 1) {
      step1.addEventListener("click", commit("setSteps", params.idx));
    } else if (params.idx === 2) {
      step2.addEventListener("click", commit("setSteps", params.idx));
    }
  },
  removeImg({ commit }, params) {
    commit;
    state.modelImgs = state.modelImgs.filter((e, i) => i != params.idx);
    if (state.modelImgs.length === 0) {
      state.modelImgs = [];
    }
    commit("setImgFiles", params.files);
  },
  enrollPart({ commit }, params) {
    commit;
    state.enrolledPart.push([params.partName, params.partImg, params.partCnt]);
  }
};

const mutations = {
  setSteps(state, idx) {
    state.step = idx;
    state.currentStep = idx;
  },
  setCurrentStep(state, idx) {
    state.currentStep = idx;
  },
  setImgFiles(state, files) {
    state.imgFiles = files;
  },
  setImage(state, imgs) {
    state.model.set_image = imgs;
  },
  setDesc(state, info) {
    state.model.set_name = info.set_name;
    state.model.theme_name = info.theme_name;
    state.model.tags = info.tags;
    state.model.description = info.description;
    state.model.reference = info.reference;
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
