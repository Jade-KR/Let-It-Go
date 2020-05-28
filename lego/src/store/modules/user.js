// import api from "../../api";

import api from "../../api";

const state = {
  photoFlag: false
};

const mutations = {
  setFlag(state, params) {
    state.photoFlag = params
  }
};

const actions = {
  async updateImg({
    commit
  }, params) {
    commit;
    var modelImgUrl = ''
    var myHeaders = new Headers();
    myHeaders.append("Authorization", "Client-ID 4d07ea22717fbd0");

    var formdata = new FormData();
    formdata.append("image", params.slice(22));

    var requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: formdata,
      redirect: "follow"
    };

    await fetch("https://api.imgur.com/3/image", requestOptions)
      .then(response => response.text())
      .then(async result => {
        const test = JSON.parse(result);
        modelImgUrl = test.data.link;
        params = {
          profile_url: modelImgUrl
        }
        await api.changProfilePic(params).then(res => console.log(res)).catch(err => console.log(err))
        localStorage.setItem("image", modelImgUrl)
        commit("setFlag", state.photoFlag === false ? true : false)
      })
      .catch(error => console.log("error", error));
  },
  async updateInfo({
    commit
  }, params) {
    commit;
    await api.updateUserInfo(params).then(res => console.log(res))
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
};