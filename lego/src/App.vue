<template>
  <div id="app">
    <route-view />
    <go-top />
  </div>
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
