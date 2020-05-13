import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import MyPage from "../views/MyPage.vue";
import Login from "../views/base/Login.vue";
import Register from "../views/base/Register.vue";
import UserSetting from "../views/UserSetting.vue";
Vue.use(VueRouter);

const routes = [{
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/mypage",
    name: "MyPage",
    component: MyPage
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/register",
    name: "Register",
    component: Register
  },
  {
    path: "/UserSetting",
    name: "UserSetting",
    component: UserSetting,
    props: true
  },

  // {
  //   path: "/about",
  //   name: "About",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/About.vue")
  // }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;