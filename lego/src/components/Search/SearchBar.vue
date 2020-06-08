<template>
  <div>
    <div id="search_bar_category" v-if="!scrollFlag">
      <div
        id="search_bar_model"
        @click="setCate(0)"
        :style="selectedCate === 0 ? selectedStyle[0] : selectedStyle[1]"
      >
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
        <i
          class="fas fa-angle-double-right checked"
          v-if="selectedCate === 2"
        ></i>
        <i class="fas fa-align-left"></i>
        테마
      </div>
    </div>
    <hr id="search_bar_divied_line" v-if="!scrollFlag" />
    <div id="serch_bar_main">
      <input
        type="text"
        id="search_bar_input"
        placeholder="검색어를 입력해주세요."
        v-model="searchWords"
        @keypress.enter="onSubmit()"
        v-if="selectedCate === 0 || selectedCate === 1"
      />
      <div v-else id="theme_autocomplete">
        <v-autocomplete
          v-model="searchWords"
          :items="themes"
          hide-details
          placeholder="검색어를 입력해주세요."
          color="rgb(255, 215, 0)"
          background-color="white"
          item-text="name"
          item-value="id"
          height="40px"
        >
        </v-autocomplete>
      </div>
      <button id="search_bar_btn" @click="onSubmit()">검색!</button>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    searchedWordByDetail: {
      type: String,
      default: ""
    },
    searchedCateByDetail: {
      type: Number,
      default: 0
    }
  },
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
      ],
      themes: [],
      scrollFlag: false,
      isMobile: false
    };
  },
  computed: {
    ...mapState({
      themesRows: state => state.search.themes
    })
  },
  watch: {
    searchedCateByDetail() {
      this.searchWords = this.searchedWordByDetail;
      this.selectedCate = this.searchedCateByDetail;
    }
  },
  created() {
    window.addEventListener("scroll", this.scrollEvent);
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.scrollEvent);
    window.removeEventListener("resize", this.onResponsiveInverted);
  },
  mounted() {
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
    this.themesRows.forEach(e => {
      this.themes.push({
        id: e[0],
        name: e[2]
      });
    });
  },
  methods: {
    onResponsiveInverted() {
      if (window.outerWidth < 600) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    },
    setCate(value) {
      if (value === 0) {
        this.selectedCate = 0;
      } else if (value === 1) {
        this.selectedCate = 1;
      } else if (value === 2) {
        this.selectedCate = 2;
      }
      this.searchWords = "";
      this.$emit("setCate", this.selectedCate);
    },
    onSubmit() {
      this.$emit("onSubmit", this.searchWords, this.selectedCate);
    },
    scrollEvent() {
      if (document.documentElement.scrollTop >= 100) {
        this.scrollFlag = true;
        document.getElementById("serch_bar_main").style.width = "100%";
      } else if (document.documentElement.scrollTop === 0) {
        this.scrollFlag = false;
        if (this.isMobile === false) {
          document.getElementById("serch_bar_main").style.width = "70%";
        } else {
          document.getElementById("serch_bar_main").style.width = "90%";
        }
      }
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
#search_bar_divied_line {
  width: 80%;
  margin: auto;
  border: 1px dashed gold;
  margin-bottom: 20px;
}
#serch_bar_main {
  width: 70%;
  margin: auto;
}
#search_bar_input {
  border: 1px solid gold;
  /* width: 500px; */
  width: 85%;
  line-height: 40px;
  font-size: 20px;
  padding-left: 20px;
}
#search_bar_btn {
  border: 1px solid gold;
  background-color: gold;
  color: white;
  /* width: 100px; */
  width: 15%;
  line-height: 40px;
  font-size: 20px;
  font-weight: 700;
}
#search_bar_btn:hover {
  background-color: green;
}
#theme_autocomplete {
  display: inline-block;
  /* width: 500px; */
  width: 85%;
  font-size: 20px;
}
@media screen and (max-width: 600px) {
  #search_bar_model,
  #search_bar_tag,
  #search_bar_theme {
    margin: 0px;
    padding: 2px;
    min-width: 100px;
  }
  #search_bar_divied_line {
    display: none;
  }
  #serch_bar_main {
    width: 90%;
  }
  #search_bar_btn:hover {
    background-color: gold;
  }
}
</style>
