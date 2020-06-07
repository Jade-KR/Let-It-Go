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
input,
button,
textarea:focus {
  outline: none;
}
</style>
