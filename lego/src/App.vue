<template>
  <v-app id="app">
    <div class="nav">
      <Nav v-if="!authFlag"></Nav>
    </div>
    <route-view
      :key="$route.fullPath"
      :style="!authFlag ? viewStyle[0] : viewStyle[1]"
    />
    <go-top :style="isMobile ? topSytle[0] : topSytle[1]" />
  </v-app>
</template>

<script>
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";
import Nav from "@/components/Nav";

import { mapState, mapActions } from "vuex";

export default {
  name: "App",

  components: {
    RouteView,
    GoTop,
    Nav
  },
  data() {
    return {
      viewStyle: [
        {
          paddingTop: "90px"
        },
        {
          paddingTop: "0px"
        }
      ],
      topSytle: [
        {
          display: "none"
        }
      ],
      isMobile: false
    };
  },
  watch: {
    isMobile() {
      if (this.isMobile === false) {
        this.viewStyle[0]["paddingTop"] = "90px";
      } else {
        this.viewStyle[0]["paddingTop"] = "20px";
      }
    }
  },
  computed: {
    ...mapState({
      authFlag: state => state.auth.authFlag
    })
  },
  async mounted() {
    await this.isTokenVerify();
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResponsiveInverted);
  },
  methods: {
    ...mapActions("auth", ["isTokenVerify"]),
    onResponsiveInverted() {
      if (window.outerWidth < 600) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    }
  }
};
</script>

<style>
#app {
  font-family: "Poor Story", cursive;
}
input,
button,
textarea:focus {
  outline: none;
}
@keyframes ldio-upeca3v4hi-1 {
  0% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(-45deg);
  }
  100% {
    transform: rotate(0deg);
  }
}
@keyframes ldio-upeca3v4hi-2 {
  0% {
    transform: rotate(180deg);
  }
  50% {
    transform: rotate(225deg);
  }
  100% {
    transform: rotate(180deg);
  }
}
.ldio-upeca3v4hi > div:nth-child(2) {
  transform: translate(-15px, 0);
}
.ldio-upeca3v4hi > div:nth-child(2) div {
  position: absolute;
  top: 40px;
  left: 40px;
  width: 120px;
  height: 60px;
  border-radius: 120px 120px 0 0;
  background: #ffdd3d;
  animation: ldio-upeca3v4hi-1 1s linear infinite;
  transform-origin: 60px 60px;
}
.ldio-upeca3v4hi > div:nth-child(2) div:nth-child(2) {
  animation: ldio-upeca3v4hi-2 1s linear infinite;
}
.ldio-upeca3v4hi > div:nth-child(2) div:nth-child(3) {
  transform: rotate(-90deg);
  animation: none;
}
@keyframes ldio-upeca3v4hi-3 {
  0% {
    transform: translate(190px, 0);
    opacity: 0;
  }
  20% {
    opacity: 1;
  }
  100% {
    transform: translate(70px, 0);
    opacity: 1;
  }
}
.ldio-upeca3v4hi > div:nth-child(1) {
  display: block;
}
.ldio-upeca3v4hi > div:nth-child(1) div {
  position: absolute;
  top: 92px;
  left: -8px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #76c93a;
  animation: ldio-upeca3v4hi-3 1s linear infinite;
}
.ldio-upeca3v4hi > div:nth-child(1) div:nth-child(1) {
  animation-delay: -0.67s;
}
.ldio-upeca3v4hi > div:nth-child(1) div:nth-child(2) {
  animation-delay: -0.33s;
}
.ldio-upeca3v4hi > div:nth-child(1) div:nth-child(3) {
  animation-delay: 0s;
}
.loadingio-spinner-bean-eater-rstzjzfll3r {
  width: 200px;
  height: 200px;
  display: inline-block;
  overflow: hidden;
  background: #ffffff;
}
.ldio-upeca3v4hi {
  width: 100%;
  height: 100%;
  position: relative;
  transform: translateZ(0) scale(1);
  backface-visibility: hidden;
  transform-origin: 0 0; /* see note above */
}
.ldio-upeca3v4hi div {
  box-sizing: content-box;
}
</style>
