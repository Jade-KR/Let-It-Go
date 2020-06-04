<template>
  <v-app id="app">
    <div class="nav">
      <Nav v-if="!authFlag"></Nav>
    </div>
    <route-view
      :key="$route.fullPath"
      :style="!authFlag ? viewStyle[0] : viewStyle[1]"
    />
    <go-top />
  </v-app>
</template>

<script>
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";
import Nav from "@/components/Nav";

import { mapState } from "vuex";

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
      ]
    };
  },
  computed: {
    ...mapState({
      authFlag: state => state.auth.authFlag
    })
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
