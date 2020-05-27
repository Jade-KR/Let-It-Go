// import api from "../../api";

const state = {};

const mutations = {};

const actions = {
  updateImg({
    commit
  }, params) {
    commit;
    console.log(params)
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

    fetch("https://api.imgur.com/3/image", requestOptions)
      .then(response => response.text())
      .then(result => {
        const test = JSON.parse(result);
        modelImgUrl = test.data.link;
        localStorage.setItem("image", modelImgUrl)
      })
      .catch(error => console.log("error", error));
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
};