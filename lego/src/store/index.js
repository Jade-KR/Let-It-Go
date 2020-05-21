import Vue from "vue";
import Vuex from "vuex";
import write from "./modules/write.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    write
  }
});
