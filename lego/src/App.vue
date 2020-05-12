<template>
  <v-app id="app">
    <route-view id="router" />
    <go-top />
  </v-app>
</template>

<script>
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";

export default {
  name: "App",

  components: {
    RouteView,
    GoTop
  },

  data: () => ({
    //
  })
};
</script>

<style></style>
