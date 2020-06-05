import LegoThemes from "../../../jsonData/LegoThemes.json";
import LegoParts from "../../../jsonData/LegoParts.json";
import LegoColors from "../../../jsonData/LegoColors.json";
import LegoCategory from "../../../jsonData/LegoCategory.json";

import api from "../../api";
import router from "../../router";

const state = {
  model: {
    theme_id: 0,
    set_images: "",
    set_name: "",
    description: "",
    tags: [],
    reference: "",
    parts: []
  },
  step: 1,
  currentStep: 1,
  modelImgs: [],
  imgFiles: "",
  themess: LegoThemes["rows"],
  descParams: {
    set_name: "",
    theme_id: null,
    tags: "",
    description: "",
    reference: ""
  },
  partList: LegoParts.rows.map((e, i) => {
    return {
      partName: e[0] + " " + e[1],
      partIdx: i,
      partImg: e[2],
      partId: e[0]
    };
  }),
  partColor: LegoColors.rows.map((color, i) => {
    return {
      colorName: color[1],
      colorRgb: color[2],
      colorId: color[0],
      colorIdx: i
    };
  }),
  enrolledPart: [],
  legoParts: LegoParts,
  legoCategory: LegoCategory,
  pickStep: 0,
  pickedParts: [],
  pickedPartByImg: [],
  pickedReset: false
};

const actions = {
  next({ commit }, params) {
    if (params.step === 1) {
      // commit("setImage", state.modelImgs);
      var modelImgUrls = [];
      var myHeaders = new Headers();
      myHeaders.append("Authorization", "Client-ID 4d07ea22717fbd0");

      for (let i = 0; i < state.modelImgs.length; ++i) {
        var formdata = new FormData();
        formdata.append("image", state.modelImgs[i].slice(22));
        var requestOptions = {
          method: "POST",
          headers: myHeaders,
          body: formdata,
          redirect: "follow"
        };

        fetch("https://api.imgur.com/3/image", requestOptions)
          .then(response => response.text())
          .then(result => {
            const test = JSON.parse(result);
            modelImgUrls.push(test.data.link);
            commit("setImage", modelImgUrls);
          });
      }
    } else if (params.step === 2) {
      commit("setDesc", params.descParams);
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
    if (params.step === 2) {
      commit("setDesc", params.descParams);
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
    if (params.partQuantity === 0) {
      return;
    }
    for (let i = 0; i < state.enrolledPart.length; ++i) {
      if (
        state.enrolledPart[i]["name"] === params.partName &&
        state.enrolledPart[i]["color"] === params.partColor
      ) {
        state.enrolledPart[i]["quantity"] =
          Number(state.enrolledPart[i]["quantity"]) +
          Number(params.partQuantity);
        return;
      }
    }
    state.enrolledPart.push({
      id: params.partId,
      name: params.partName,
      img: params.partImg,
      color: params.partColor,
      colorId: params.partColorId,
      quantity: params.partQuantity
    });
  },
  deletePart({ commit }, params) {
    commit;
    state.enrolledPart = state.enrolledPart.filter(e => {
      return e["name"] !== params.partName || e["color"] !== params.partColor;
    });
  },
  filterParts({ commit }, params) {
    let filteredParts = LegoParts.rows.filter(part => {
      return part[5] === params;
    });
    commit("setPickedParts", filteredParts);
  },
  changeStep({ commit }, params) {
    commit("setPickStep", params);
  },
  pickPartBytImg({ commit }, params) {
    const part = [
      params["part"][0] + " " + params["part"][1],
      params["part"][2],
      params["part"][0]
    ];
    // for (let i = 0; i < state.pickedPartByImg.length; ++i) {
    //   if (params["part"][0] === state.pickedPartByImg[i][2]) {
    //     return;
    //   }
    // }

    if (params["isHave"] === true) {
      const temp = [];
      for (let i = 0; i < state.pickedPartByImg.length; ++i) {
        if (state.pickedPartByImg[i][2] === params["part"][0]) {
          continue;
        }
        temp.push(state.pickedPartByImg[i]);
      }
      commit("resetOnlyPickedPartByImg");
      for (let i = 0; i < temp.length; ++i) {
        commit("setPickedPartByImg", temp[i]);
      }
      return;
    }

    commit("setPickedPartByImg", part);
  },
  async onWriteSubmit({ commit }) {
    const imgUrlList = state.model.set_images;
    var imgUrlString = "";
    imgUrlList.forEach((e, i) => {
      if (i === imgUrlList.length - 1) {
        imgUrlString += String(e);
        return;
      }
      imgUrlString += String(e) + "|";
    });
    commit("setImage", imgUrlString);

    const tagList = state.model.tags;
    var tagString = "";
    tagList.forEach((e, i) => {
      if (i === tagList.length - 1) {
        tagString += String(e);
        return;
      }
      tagString += String(e) + "|";
    });
    commit("setTags", tagString);
    commit("setParts");
    await api
      .writeSubmit(state.model)
      .then(res => {
        res;
        alert("글이 성공적으로 작성되었습니다.");
        router.push("/");
        location.reload();
      })
      .catch(err => {
        err;
        alert("글 작성에 문제가 생겼습니다.");
      });
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
    state.model.set_images = imgs;
  },
  setDesc(state, info) {
    state.model.set_name = info.set_name;
    state.model.theme_id = info.theme_id;
    state.model.tags = info.tags;
    state.model.description = info.description;
    state.model.reference = info.reference;
  },
  setTags(state, tagString) {
    state.model.tags = tagString;
  },
  setParts(state) {
    state.enrolledPart.forEach(e => {
      state.model.parts.push({
        part_id: e["id"],
        color_id: Number(e["colorId"]),
        quantity: e["quantity"]
      });
    });
  },
  setPickStep(state, step) {
    state.pickStep = step;
  },
  setPickedParts(state, result) {
    state.pickedParts = result;
  },
  setPickedPartByImg(state, part) {
    state.pickedPartByImg.push(part);
  },
  resetPickedPartByImg(state) {
    state.pickedPartByImg = [];
    state.pickedReset = state.pickedReset === false ? true : false;
  },
  resetOnlyPickedPartByImg(state) {
    state.pickedPartByImg = [];
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
