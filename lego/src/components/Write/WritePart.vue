<template>
  <div @click="test()">asdf</div>
</template>

<script>
import LegoParts from "../../../jsonData/LegoParts.json";

export default {
  data() {
    return {
      partsList: LegoParts["rows"],
      partsHeader: LegoParts["header"]
    };
  },
  methods: {
    test() {
      console.log(this.partsList);
      console.log(this.partsHeader);
    }
  }
};
</script>

<style scoped></style>
