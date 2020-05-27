<template>
  <div id="search_box">
    <div id="search_bar">
      <search-bar></search-bar>
    </div>
    <div id="search_card">
      <search-card></search-card>
    </div>
  </div>
</template>

<script>
import SearchBar from "../../components/Search/SearchBar.vue";
import SearchCard from "../../components/Search/SearchCard.vue";

export default {
  components: {
    SearchBar,
    SearchCard
  }
};
</script>

<style scoped>
#search_box {
  width: 850px;
  margin: auto;
  margin-top: 20px;
}
#search_bar {
  border: 3px solid gold;
  padding: 20px;
  text-align: center;
  margin-bottom: 20px;
  position: sticky;
  top: 90px;
  background-color: white;
}
#search_card {
}
</style>
