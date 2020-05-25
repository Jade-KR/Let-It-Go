import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import MyPage from "../views/MyPage.vue";
import Login from "../views/base/Login.vue";
import Register from "../views/base/Register.vue";
import Detail from "../views/Page/Detail.vue";
import UserSetting from "../views/UserSetting.vue";
import Write from "../views/Page/Write.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/mypage/:user_id",
    name: "MyPage",
    component: MyPage,
    meta: {
      authRequired: true
    }
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
    path: "/detail/:modelId",
    name: "Detail",
    component: Detail
  },
  {
    path: "/UserSetting",
    name: "UserSetting",
    component: UserSetting,
    props: true,
    meta: {
      authRequired: true
    }
  },
  {
    path: "/write",
    name: "Write",
    component: Write,
    meta: {
      authRequired: true
    }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach(function(to, from, next) {
  const user_pk = localStorage.getItem("pk");
  if (
    to.matched.some(function(routeInfo) {
      return routeInfo.meta.authRequired;
    })
  ) {
    if (user_pk) {
      next();
    } else {
      alert("로그인을 해주세요");
      router.push("/login");
    }
  } else {
    next();
  }
});

export default router;
