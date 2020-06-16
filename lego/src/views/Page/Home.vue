<template>
  <div
    id="home_body"
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <div id="home_show">
      <div v-if="!isCate">
        <user-category @cateSubmit="cateSubmit">
          <span slot="userCategory" id="userCategory" />
        </user-category>
      </div>
      <div
        @click="styleCheck()"
        v-if="styleFlag === false"
        class="home_show_btn"
      >
        모아보기
      </div>
      <div v-else @click="styleCheck()" class="home_show_btn">크게보기</div>
    </div>
    <div v-if="!isCate && homeCate === 3" id="home_no_show">
      선호 카테고리를 선택해 주세요
    </div>
    <div :style="styleFlag ? matrixWidth : instaWidth" v-else>
      <div
        class="home_card"
        v-for="(model, i) in models"
        :key="`model-${i}`"
        :style="styleFlag ? matrixStyle : instaStyle"
      >
        <home-card
          :idx="i"
          :id="model.id"
          :images="model.images"
          :nickname="model.nickname"
          :name="model.name"
          :isLike="model.is_like"
          :styleFlag="styleFlag"
          :likeCount="model.like_count"
        />
      </div>
    </div>
  </div>
</template>

<script>
import HomeCard from "@/components/Home/HomeCard";
import UserCategory from "@/components/Home/UserCategory";
import { mapState, mapActions, mapMutations } from "vuex";

export default {
  name: "Home",
  components: {
    HomeCard,
    UserCategory
  },
  data() {
    return {
      loading: true,
      styleFlag: false,
      isCate: true,
      matrixWidth: {
        width: "70vw",
        margin: "auto",
        textAlign: "center"
      },
      instaWidth: {},
      matrixStyle: {
        border: "5px solid gold",
        width: "250px",
        display: "inline-block",
        margin: "30px",
        backgroundColor: "white"
      },
      instaStyle: {
        border: "5px solid gold",
        width: "614px",
        margin: "30px auto",
        backgroundColor: "white"
      },
      isMobile: false,
      homeState: 0
    };
  },
  computed: {
    ...mapState({
      homeCate: state => state.home.homeCate,
      models: state => state.home.modelList,
      page: state => state.home.modelPage,
      likePage: state => state.home.likeModelPage,
      recommendPage: state => state.home.recommendModelPage,
      modelAllCnt: state => state.home.modelAllCnt,
      likeModelAllCnt: state => state.home.likeModelAllCnt,
      recommendModelAllCnt: state => state.home.recommendModelAllCnt,
      isCategory: state => state.auth.isCategory
    })
  },
  watch: {
    isMobile() {
      if (this.isMobile === false) {
        this.instaStyle["width"] = "614px";
      } else {
        this.instaStyle["width"] = "100%";
      }
    },
    async homeCate() {
      const bodyContainer = document.querySelector("#home_body");
      bodyContainer.classList.add("anim-out");
      setTimeout(async () => {
        await this.resetModels();
        await this.resetPages();
        const params = {
          page: 1,
          append: false
        };
        if (this.homeCate === 1) {
          await this.getModels(params);
        } else if (this.homeCate === 2) {
          await this.getLikeModels(params);
        } else if (this.homeCate === 3) {
          await this.getRecommendModels(params);
        }
        bodyContainer.classList.remove("anim-out");
        this.loading = false;
      }, 300);
    }
  },
  async mounted() {
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
    if (localStorage.getItem("categories") === "null") {
      await this.setCate();
      document.getElementById("userCategory").click();
    }
    const params = {
      page: 1,
      append: false
    };
    if (this.homeCate === 1) {
      await this.getModels(params);
    } else if (this.homeCate === 2) {
      await this.getLikeModels(params);
    } else if (this.homeCate === 3) {
      await this.getRecommendModels(params);
    }
    this.loading = false;
  },
  beforeDestroy() {
    this.resetModels();
    window.removeEventListener("resize", this.onResponsiveInverted);
  },
  methods: {
    ...mapActions("home", ["getModels", "getLikeModels", "getRecommendModels"]),
    ...mapMutations("home", ["resetModels", "resetPages"]),
    onResponsiveInverted() {
      if (window.outerWidth < 600) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    },
    styleCheck() {
      if (this.styleFlag === false) {
        this.styleFlag = true;
      } else {
        this.styleFlag = false;
      }
    },
    async loadMore() {
      this.loading = true;
      const params = {
        append: true
      };
      if (this.homeCate === 1) {
        if (this.modelAllCnt === Number(this.page)) {
          return;
        }
        params["page"] = this.page;
        await this.getModels(params);
      } else if (this.homeCate === 2) {
        if (this.likeModelAllCnt === Number(this.likePage)) {
          return;
        }
        params["page"] = this.likePage;
        await this.getLikeModels(params);
      } else if (this.homeCate === 3) {
        if (this.recommendModelAllCnt === Number(this.recommendPage)) {
          return;
        }
        params["page"] = Number(this.recommendPage);
        await this.getRecommendModels(params);
      }
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    },
    setCate() {
      this.isCate = false;
    },
    cateSubmit(value) {
      this.isCate = value;
    }
  }
};
</script>

<style scoped>
#home_body {
  box-sizing: border-box;
  width: 100%;
  opacity: 1;
  transition: all 0.3s ease-out;
}
#home_body.anim-out {
  opacity: 0;
  transform: scale(0.9) translateY(40px);
}
#home_show {
  width: 120px;
  padding: 10px;
  text-align: center;
  position: sticky;
  top: 70px;
  float: right;
}
.home_show_btn {
  cursor: pointer;
  background-color: gold;
  line-height: 50px;
  color: white;
  font-weight: 600;
  font-size: 20px;
}
#home_no_show {
  text-align: center;
  margin-top: 100px;
  font-size: 50px;
  font-weight: 700;
  transform: translateX(50px);
}

@media screen and (max-width: 600px) {
  #home_body {
    box-sizing: border-box;
    width: 100%;
  }
  #home_show {
    display: none;
  }
  #home_no_show {
    text-align: center;
    margin-top: 100px;
    font-size: 50px;
    font-weight: 700;
    transform: translateX(50px);
  }
}
</style>
