<template>
  <v-app>
    <route-view />
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
