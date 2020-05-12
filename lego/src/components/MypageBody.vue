<template>
  <div>
    <div class="container">
      <div class="row">
        <div class="item"></div>
        <div class="item"></div>
        <div class="item"></div>
      </div>
      <div class="row">
        <div class="item"></div>
        <div class="item"></div>
        <div class="item"></div>
      </div>
      <div class="row">
        <div class="item"></div>
        <div class="item"></div>
        <div class="item"></div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {};
  }
};
</script>

<style scoped>
.container {
  height: 100%;
  width: 100%;
}
.row {
  display: flex;
  border: solid 1px black;
  height: 100%;
  margin-bottom: 20px;
}
.item:nth-child(-n + 2) {
  margin-right: 20px;
}
.item {
  background: yellow;
  width: 250px;
  height: 250px;
}
</style>
