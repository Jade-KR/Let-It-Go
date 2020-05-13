<template>
  <v-app id="app">
    <div class="nav">
      <Nav></Nav>
    </div>
    <route-view :key="$route.fullPath" />
    <go-top />
  </v-app>
</template>

<script>
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";
import Nav from "@/components/Nav";

export default {
  name: "App",

  components: {
    RouteView,
    GoTop,
    Nav
  },

  data: () => ({
    //
  })
};
</script>

<style scoped>
.nav {
  width: 100%;
  /* height: 100%; */
  padding-bottom: 10px;
  border-bottom: rgb(255, 213, 26) solid 4px;
}
</style>
