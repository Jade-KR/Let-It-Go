import api from "../../api";

const state = {
  modelPage: "1",
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
  userPage: "1",
  user: {
    id: 0,
    username: "",
    email: "",
    nickname: "",
    age: 0,
    gender: 0,
    is_staff: false,
    is_active: true,
    last_login: ""
  },
  userList: []
};

const actions = {
  async getModels({ commit }, params) {
    const append = params.append;
    const resp = await api.getModels(params).then(res => res.data);
    const models = resp.results.map(e => e);
    if (append) {
      commit("addModelList", models);
    } else {
      commit("setModels", models);
    }
    if (resp.next === null) {
      return;
    }
    commit("setModelPage", resp.next);
  },
  async deleteModel({ commit }, params) {
    const resp = await api
      .delelteModel(params)
      .then(res => res.data)
      .catch(err => err.response);
    if (resp === "삭제 완료") {
      const temp = [];
      for (let i = 0; i < state.modelList.length; ++i) {
        if (state.modelList[i].id !== params) {
          temp.push(state.modelList[i]);
        }
      }
      commit("setModels", temp);
    }
  },
  async getUsers({ commit }, params) {
    const append = params.append;
    const resp = await api.getUsers(params).then(res => res.data);
    if (resp.results.length !== 0 && state.userList.length !== 0) {
      if (resp.results[0].id === state.userList[0].id) {
        return;
      }
    }
    const users = [];
    for (let i = 0; i < resp.results.length; ++i) {
      if (resp.results[i].is_active !== false) {
        users.push(resp.results[i]);
      }
    }
    if (append) {
      commit("addUserList", users);
    } else {
      commit("setUsers", users);
    }
    if (resp.next === null) {
      return;
    }
    commit("setUserPage", resp.next);
  },
  async deleteUser({ commit }, params) {
    const resp = await api
      .delelteUser(params)
      .then(res => res.data)
      .catch(err => err.response);
    if (resp === "블럭 성공") {
      const temp = [];
      for (let i = 0; i < state.userList.length; ++i) {
        if (state.userList[i].id !== params) {
          temp.push(state.userList[i]);
        }
      }
      commit("setUsers", temp);
    }
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
    state.modelPage = new URL(url).searchParams.get("page");
  },
  setUsers(state, user) {
    state.userList = user.map(e => e);
  },
  addUserList(state, user) {
    state.userList = user.userList.concat(user);
  },
  setUserPage(state, url) {
    state.userPage = new URL(url).searchParams.get("page");
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
