<template>
  <div
    id="search_box"
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <div id="search_bar">
      <search-bar
        @onSubmit="onSubmit"
        @setCate="setCate"
        :searchedWordByDetail="searchedWordByDetail"
        :searchedCateByDetail="searchedCateByDetail"
      ></search-bar>
    </div>
    <div id="search_card_box">
      <div v-for="(model, i) in models" :key="`model-${i}`" id="search_card">
        <search-card
          :id="model.id"
          :image="model.images"
          :name="model.name"
          :nickname="model.nickname"
          :isLike="model.is_like"
          :likeCount="model.like_count"
          :reviewCount="model.review_count"
          :isReview="model.is_review"
        ></search-card>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "../../components/Search/SearchBar.vue";
import SearchCard from "../../components/Search/SearchCard.vue";
import { mapState, mapActions, mapMutations } from "vuex";

export default {
  components: {
    SearchBar,
    SearchCard
  },
  data() {
    return {
      loading: true,
      selectedCate: 0,
      selectedTheme: 0,
      searchedWordByDetail: "",
      searchedCateByDetail: 0
    };
  },
  computed: {
    ...mapState({
      models: state => state.search.modelList,
      page: state => state.search.modelPage,
      endPoint: state => state.search.endPoint,
      searchWordByDetail: state => state.search.searchWordByDetail,
      searchCateByDetail: state => state.search.searchCateByDetail,
      searchByDetailFlag: state => state.search.searchByDetailFlag
    })
  },
  async mounted() {
    if (this.searchByDetailFlag === true) {
      window.scrollTo(0, 0);
      this.resetEndPoint();
      this.resetModelList();
      this.selectedTheme = this.searchWordByDetail;
      this.searchedWordByDetail = String(this.searchWordByDetail);
      if (this.searchCateByDetail === "tag") {
        this.selectedCate = 1;
        this.searchedCateByDetail = 1;
      } else {
        this.selectedCate = 2;
        this.searchedCateByDetail = 2;
      }
      const params = {
        append: false,
        page: 1
      };
      if (this.searchCateByDetail === "tag") {
        params["tag"] = this.searchWordByDetail;
      } else if (this.searchCateByDetail === "theme") {
        params["theme"] = this.searchWordByDetail;
      }
      const result = await this.getModels(params);
      if (result === false) {
        alert("검색결과 없음");
        return;
      }
      if (this.endPoint === true) {
        return;
      }
      this.loading = false;

      this.resetSearchByDetailFlag();
    }
  },
  beforeDestroy() {
    this.resetModelList();
  },
  methods: {
    ...mapActions("search", ["getModels"]),
    ...mapMutations("search", [
      "resetEndPoint",
      "resetModelList",
      "resetSearchByDetailFlag"
    ]),
    setCate(value) {
      this.loading = true;
      this.selectedCate = value;
    },
    async onSubmit(words, cate) {
      if (words === " " || words === "  " || words.length === 0) {
        alert("검색어를 입력해주세요.");
        return;
      }
      window.scrollTo(0, 0);
      this.resetEndPoint();
      this.resetModelList();
      this.selectedTheme = words;
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
      const result = await this.getModels(params);
      if (result === false) {
        alert("검색결과 없음");
        return;
      }
      if (this.endPoint === true) {
        return;
      }
      this.loading = false;
    },
    async loadMore() {
      this.loading = true;
      if (this.models.length === 0) {
        return;
      }
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
        params["theme"] = this.selectedTheme;
      }
      await this.getModels(params);
      if (this.endPoint === true) {
        return;
      }
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
  top: 50px;
  background-color: white;
  z-index: 10;
  transition: 0.3s ease-in-out all;
}
#search_card_box {
  width: 100%;
  height: 100%;
}
#search_card {
  display: inline-block;
}
@media screen and (max-width: 600px) {
  #search_box {
    width: 100%;
  }
  #search_bar {
    padding: 5px;
    top: 38px;
  }
  #search_card_box {
    margin-bottom: 40px;
  }
}
</style>
