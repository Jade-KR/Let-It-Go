<template>
  <v-app id="app">
    <div class="nav">
      <Nav></Nav>
    </div>
    <route-view :key="$route.fullPath" style="padding-top: 90px;" />
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

<style>
input,
button,
textarea:focus {
  outline: none;
}
</style>