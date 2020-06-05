import Vue from "vue";
import Vuex from "vuex";
import write from "./modules/write.js";
import Parts from "./modules/Parts.js";
import auth from "./modules/auth.js";
import home from "./modules/home.js";
import detail from "./modules/detail.js";
import mypage from "./modules/mypage.js";
import user from "./modules/user.js";
import search from "./modules/search.js";
import admin from "./modules/admin.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    write,
    Parts,
    auth,
    home,
    detail,
    mypage,
    user,
    search,
    admin
  }
});
