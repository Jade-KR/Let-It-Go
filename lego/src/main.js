import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import infiniteScroll from "vue-infinite-scroll";
import "./plugins/vee-validate";
import JsonExcel from "vue-json-excel";

Vue.config.productionTip = false;

Vue.use(infiniteScroll);
Vue.component("downloadExcel", JsonExcel);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
