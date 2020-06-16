import api from "../../api";

const state = {
  photoFlag: false
};

const mutations = {
  setFlag(state, params) {
    state.photoFlag = params;
  }
};

const actions = {
  async updateImg({ commit }, params) {
    var modelImgUrl = "";

    var formdata = new FormData();
    formdata.append("image", params);
    await api.uploadImage(formdata).then(async response => {
      modelImgUrl = response.data;
      params = {
        profile_url: modelImgUrl
      };
      await api.changeProfilePic(params);
      localStorage.setItem("image", modelImgUrl);
      commit("setFlag", state.photoFlag === false ? true : false);
    });
  },
  async updateInfo({ commit }, params) {
    commit;
    const resp = await api.updateUserInfo(params).then(res => res.data);
    return resp;
  },
  async deleteImg({ commit }, params) {
    const imgUrl = null;
    params = {
      profile_url: imgUrl
    };
    await api.changeProfilePic(params);
    localStorage.setItem("image", imgUrl);
    commit("setFlag", state.photoFlag === false ? true : false);
  },
  async getPartsFromLegoRail({ commit }) {
    commit;
    const resp = await api.getPartsFromLegoRail();
    const items = resp.data;
    return items;
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
