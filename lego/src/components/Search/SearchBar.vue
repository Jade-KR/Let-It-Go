<template>
  <div>
    <div id="search_bar_category">
      <div
        id="search_bar_model"
        @click="setCate(0)"
        :style="selectedCate === 0 ? selectedStyle[0] : selectedStyle[1]"
      >
        <!-- <i class="fas fa-check checked" v-if="selectedCate === 0"></i> -->
        <i
          class="fas fa-angle-double-right checked"
          v-if="selectedCate === 0"
        ></i>
        <i class="fas fa-scroll"></i>
        설계도
      </div>
      <div
        id="search_bar_tag"
        @click="setCate(1)"
        :style="selectedCate === 1 ? selectedStyle[0] : selectedStyle[1]"
      >
        <!-- <i class="fas fa-check checked" v-if="selectedCate === 1"></i> -->
        <i
          class="fas fa-angle-double-right checked"
          v-if="selectedCate === 1"
        ></i>
        <i class="fas fa-tags"></i>
        태그
      </div>
      <div
        id="search_bar_theme"
        @click="setCate(2)"
        :style="selectedCate === 2 ? selectedStyle[0] : selectedStyle[1]"
      >
        <!-- <i class="fas fa-check checked" v-if="selectedCate === 2"></i> -->
        <i
          class="fas fa-angle-double-right checked"
          v-if="selectedCate === 2"
        ></i>
        <i class="fas fa-align-left"></i>
        테마
      </div>
    </div>
    <hr id="search_bar_divied_line" />
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
          color: "black",
          fontSize: "20px"
        },
        {
          color: "gray",
          fontSize: "18px"
        }
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
  margin-bottom: 10px;
}
.checked {
  margin-right: 5px;
  color: skyblue;
  font-size: 24px;
}
#search_bar_model,
#search_bar_tag,
#search_bar_theme {
  display: inline-block;
  padding: 5px;
  font-size: 18px;
  min-width: 120px;
  margin: 0 50px;
  cursor: pointer;
  font-weight: 600;
  color: gray;
}
/* #search_bar_model {
  border: 1px solid gold;
}
#search_bar_tag {
  border: 1px solid green;
}
#search_bar_theme {
  border: 1px solid red;
} */
/* #search_bar_model:hover {
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
} */
#search_bar_divied_line {
  width: 80%;
  margin: auto;
  border: 1px dashed gold;
  margin-bottom: 20px;
}
#search_bar_input {
  border: 1px solid gold;
  width: 500px;
  line-height: 40px;
  font-size: 20px;
  padding-left: 20px;
}
#search_bar_btn {
  border: 1px solid gold;
  background-color: gold;
  color: white;
  width: 100px;
  line-height: 40px;
  font-size: 20px;
  font-weight: 700;
}
#search_bar_btn:hover {
  background-color: green;
}
</style>
