<template>
  <div>
    <div id="search_bar_category">
      <div
        id="search_bar_model"
        @click="setCate(0)"
        :style="selectedCate === 0 ? selectedStyle[0] : selectedStyle[3]"
      >
        <i class="fas fa-check checked" v-if="selectedCate === 0"></i>
        설계도
      </div>
      <div
        id="search_bar_tag"
        @click="setCate(1)"
        :style="selectedCate === 1 ? selectedStyle[1] : selectedStyle[3]"
      >
        <i class="fas fa-check checked" v-if="selectedCate === 1"></i>
        태그
      </div>
      <div
        id="search_bar_theme"
        @click="setCate(2)"
        :style="selectedCate === 2 ? selectedStyle[2] : selectedStyle[3]"
      >
        <i class="fas fa-check checked" v-if="selectedCate === 2"></i>
        테마
      </div>
    </div>
    <div id="serch_bar_main">
      <input
        type="text"
        id="search_bar_input"
        placeholder="검색어를 입력해주세요."
        v-model="searchWords"
        @keypress.enter="onSubmit(searchWords)"
      />
      <button id="search_bar_btn" @click="onSubmit(searchWords)">검색!</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchWords: "",
      selectedCate: 0,
      selectedStyle: [
        {
          color: "white",
          backgroundColor: "gold"
        },
        {
          color: "white",
          backgroundColor: "green"
        },
        {
          color: "white",
          backgroundColor: "red"
        }
        // {
        //   color: "black",
        //   backgroundColor: "white"
        // }
      ]
    };
  },
  methods: {
    setCate(value) {
      if (value === 0) {
        this.selectedCate = 0;
      } else if (value === 1) {
        this.selectedCate = 1;
      } else if (value === 2) {
        this.selectedCate = 2;
      }
    },
    onSubmit(value) {
      if (
        this.searchWords === " " ||
        this.searchWords === "  " ||
        this.searchWords.length === 0
      ) {
        alert("검색어를 입력해주세요.");
      }
      console.log(value);
      console.log(this.selectedCate);
    }
  }
};
</script>

<style scoped>
#search_bar_category {
  margin-bottom: 20px;
}
.checked {
  margin-right: 5px;
}
#search_bar_model,
#search_bar_tag,
#search_bar_theme {
  display: inline-block;
  padding: 5px;
  font-size: 20px;
  min-width: 120px;
  margin: 0 50px;
  cursor: pointer;
}
#search_bar_model {
  border: 1px solid gold;
}
#search_bar_tag {
  border: 1px solid green;
}
#search_bar_theme {
  border: 1px solid red;
}
#search_bar_model:hover {
  background-color: gold;
  color: white;
}
#search_bar_tag:hover {
  background-color: green;
  color: white;
}
#search_bar_theme:hover {
  background-color: red;
  color: white;
}
#search_bar_input {
  border: 1px solid skyblue;
  width: 500px;
  line-height: 40px;
  font-size: 20px;
  padding-left: 20px;
}
#search_bar_btn {
  border: 1px solid skyblue;
  background-color: skyblue;
  color: white;
  width: 100px;
  line-height: 40px;
  font-size: 20px;
  font-weight: 700;
}
</style>
