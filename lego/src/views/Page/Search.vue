<template>
  <div
    id="search_box"
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <div id="search_bar">
      <search-bar @onSubmit="onSubmit" @setCate="setCate"></search-bar>
    </div>
    <div id="search_card_box">
      <div v-for="(model, i) in models" :key="`model-${i}`" id="search_card">
        <search-card
          :id="model.id"
          :image="model.images"
          :name="model.name"
          :nickname="model.nickname"
        ></search-card>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "../../components/Search/SearchBar.vue";
import SearchCard from "../../components/Search/SearchCard.vue";
import { mapState, mapActions } from "vuex";

export default {
  components: {
    SearchBar,
    SearchCard
  },
  data() {
    return {
      loading: true
    };
  },
  computed: {
    ...mapState({
      models: state => state.search.modelList,
      page: state => state.search.modelPage
    })
  },
  methods: {
    ...mapActions("search", ["getModels"]),
    setCate() {
      this.loading = true;
    },
    async onSubmit(words, cate) {
      if (words === " " || words === "  " || words.length === 0) {
        alert("검색어를 입력해주세요.");
        return;
      }
      const params = {
        append: false,
        page: 1
      };
      if (cate === 0) {
        params["name"] = words;
      } else if (cate === 1) {
        params["tag"] = words;
      } else if (cate === 2) {
        params["theme"] = words;
      }
      // console.log(params);
      const result = await this.getModels(params);
      if (result === false) {
        alert("검색결과 없음");
      }
      this.loading = false;
    },
    async loadMore() {
      this.loading = true;
      const setName = this.models[this.models.length - 1]["name"];
      const params = {
        page: this.page,
        append: true
      };
      if (this.selectedCate === 0) {
        params["name"] = setName;
      } else if (this.selectedCate === 1) {
        params["tag"] = setName;
      } else if (this.selectedCate === 2) {
        params["theme"] = setName;
      }
      await this.getModels(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    }
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
  z-index: 10;
}
#search_card_box {
  width: 100%;
  height: 100%;
}
#search_card {
  display: inline-block;
}
</style>
