<template>
  <div class="home_card_body">
    <div class="home_card_header">{{ name }}</div>
    <div class="home_card_imgs" v-if="imgFlag === true">
      <div class="slideshow_container">
        <div
          v-for="(url, i) in imageList"
          :key="`url-${i}`"
          @click="goDetail(id)"
          style="cursor: pointer;"
        >
          <div :class="`mySlides${idx} fade`" :id="`mySlide-${i}`">
            <img
              src="../../assets/icons/no_img.jpg"
              :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
              :id="`slideImg-${i}-${idx}`"
              v-if="!images"
            />
            <img
              :src="url"
              alt
              :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
              :id="`slideImg-${i}-${idx}`"
              v-else
              @load="showSlides(1), onResizeHeight()"
              @error="imgError()"
            />
          </div>
        </div>

        <a class="prev" @click.stop="plusSlides(-1)">&#10094;</a>
        <a class="next" @click.stop="plusSlides(1)">&#10095;</a>
      </div>
    </div>
    <div class="home_card_imgs" v-else>
      <div class="slideshow_container">
        <div
          class="go_detail_btn"
          @click="goDetail(id)"
          :style="styleFlag ? matrixStyle[4] : instaStyle[4]"
        >
          상세보기
        </div>
        <img
          src="../../assets/icons/no_img.jpg"
          :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
        />
      </div>
    </div>
    <div
      class="home_card_footer"
      :style="styleFlag ? matrixStyle[1] : instaStyle[1]"
    >
      <div :style="styleFlag ? matrixStyle[0] : instaStyle[5]">
        <div
          :style="styleFlag ? matrixStyle[5] : instaStyle[0]"
          v-for="i in imageLength"
          :key="`dots-${i}`"
        >
          <span :class="`dot${idx} dotdot`" @click="currentSlide(i + 1)"></span>
        </div>
      </div>
      <div
        :style="styleFlag ? matrixStyle[2] : instaStyle[2]"
        v-if="isMobile === false"
      >
        <div class="home_card_footer_director">Director. {{ nickname }}</div>
        <div
          class="home_card_footer_btns"
          :data-test="`${likeCnt}명이 좋아합니다.`"
        >
          <button v-if="like" class="home_card_like" @click="pushLike()">
            <i class="fas fa-heart" />
          </button>
          <button v-else class="home_card_like" @click="pushLike()">
            <i class="far fa-heart" />
          </button>
        </div>
      </div>

      <div :style="styleFlag ? matrixStyle[2] : instaStyle[2]" v-else>
        <div class="home_card_footer_btns">
          <button v-if="like" class="home_card_like" @click="pushLike()">
            <i class="fas fa-heart" />
          </button>
          <button v-else class="home_card_like" @click="pushLike()">
            <i class="far fa-heart" />
          </button>
          <div v-if="isMobile" class="home_card_like_cnt">
            {{ likeCnt }}명이 좋아합니다.
          </div>
        </div>
        <hr style="border: 0.2px solid gold" />
        <div class="home_card_footer_director">Director. {{ nickname }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router";
import { mapActions } from "vuex";

export default {
  props: {
    idx: {
      type: Number,
      default: 0
    },
    styleFlag: {
      type: Boolean,
      default: false
    },
    id: {
      type: Number,
      default: 0
    },
    images: {
      type: String,
      default: ""
    },
    name: {
      type: String,
      default: ""
    },
    nickname: {
      type: String,
      default: ""
    },
    isLike: {
      type: Number,
      default: -1
    },
    likeCount: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      imgFlag: true,
      like: false,
      slideIndex: 1,
      imageList: ["images/icons/no_img.jpg"],
      imageLength: 0,
      likeCnt: 0,
      matrixStyle: [
        {
          display: "block"
        },
        {
          padding: "5px",
          display: "block",
          textAlign: "center"
        },
        {
          width: "100%",
          display: "flex"
        },
        {
          width: "100%",
          height: "250px"
        },
        {
          left: "80%"
        },
        {
          display: "inline-block"
        }
      ],
      instaStyle: [
        {
          display: "inline-block"
        },
        {
          padding: "10px",
          display: "flex"
        },
        {
          width: "100%",
          display: "flex"
        },
        {
          width: "100%"
        },
        {
          left: "87.7%"
        },
        {
          position: "absolute",
          right: "50%",
          transform: "translateX(50%)"
        }
      ],
      isMobile: false
    };
  },
  watch: {
    imageList() {
      this.imageLength = this.imageList.length;
    },
    isMobile() {
      this.onResizeHeight();
      if (this.isMobile === false) {
        this.instaStyle[2]["display"] = "flex";
      } else {
        this.instaStyle[2]["display"] = "block";
      }
    }
  },
  async mounted() {
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
    if (this.isLike === 0) {
      this.like = false;
    } else {
      this.like = true;
    }
    if (this.images) {
      this.imageList = await this.images.split("|");
    }
    this.likeCnt = this.likeCount;
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResponsiveInverted);
  },
  methods: {
    ...mapActions("home", ["onLike"]),
    onResponsiveInverted() {
      if (window.outerWidth < 600) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    },
    imgError() {
      this.imgFlag = false;
    },
    onResizeHeight() {
      if (this.isMobile === false) {
        if (this.styleFlag == true) {
          for (let i = 0; i < this.imageList.length; ++i) {
            document.getElementById(`slideImg-${i}-${this.idx}`).style.height =
              "250px";
          }
          return;
        }
        var maxHeight = 0;
        // var minHeight = 614;
        for (let i = 0; i < this.imageList.length; ++i) {
          var naturalHeight = document.getElementById(
            `slideImg-${i}-${this.idx}`
          ).naturalHeight; // img 높이
          if (maxHeight < naturalHeight) {
            maxHeight = naturalHeight;
          }
          // if (minHeight > naturalHeight) {
          //   minHeight = naturalHeight;
          // }
        }
        if (maxHeight > 614) {
          maxHeight = 614;
        }
        // if (minHeight < 200) {
        //   minHeight = 300;
        // }
        for (let i = 0; i < this.imageList.length; ++i) {
          document.getElementById(`slideImg-${i}-${this.idx}`).style.height =
            String(maxHeight) + "px";
          // String(minHeight) + "px";
        }
      } else {
        for (let i = 0; i < this.imageList.length; ++i) {
          document.getElementById(`slideImg-${i}-${this.idx}`).style.height =
            "365px";
        }
      }
    },
    goDetail() {
      window.scrollTo(0, 0);
      router.push("/detail" + "/" + this.id);
    },
    async pushLike() {
      const params = {
        set_id: this.id
      };
      const result = await this.onLike(params);
      if (result === "좋아요") {
        this.like = true;
        this.likeCnt += 1;
      } else if (result === "좋아요 취소") {
        this.like = false;
        this.likeCnt -= 1;
      }
    },
    plusSlides(n) {
      this.showSlides((this.slideIndex += n));
    },
    currentSlide(n) {
      this.showSlides((this.slideIndex = n));
    },
    showSlides(n) {
      var i;
      var slides = document.getElementsByClassName(`mySlides${this.idx}`);
      var dots = document.getElementsByClassName(`dot${this.idx}`);
      if (n > slides.length) {
        this.slideIndex = 1;
      }
      if (n < 1) {
        this.slideIndex = slides.length;
      }
      for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
      }
      for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
      }
      slides[this.slideIndex - 1].style.display = "block";
      dots[this.slideIndex - 1].className += " active";
    }
  }
};
</script>

<style scoped>
.home_card_body {
  text-align: initial;
}
.home_card_header {
  padding: 10px;
  padding-left: 15px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 18px;
  font-weight: 700;
}
.home_card_imgs {
  border-top: 5px solid gold;
  border-bottom: 5px solid gold;
}

.home_card_footer_director {
  padding: 5px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: start;
}
.home_card_footer_btns:hover::after {
  content: attr(data-test);
  position: absolute;
  transform: translate(30px, 2px);
  font-size: 20px;
  background-color: white;
  border: 1px solid gold;
  padding: 5px 10px;
}
.home_card_like {
  color: red;
  font-size: 25px;
  float: right;
}
.go_detail_btn {
  position: absolute;
  cursor: pointer;
  background-color: rgba(255, 215, 0, 0.5);
  color: black;
  font-weight: 700;
  padding: 5px;
  text-align: center;
  z-index: 5;
}
.go_detail_btn:hover {
  background-color: gold;
  color: white;
}
.mySlides {
  display: none;
}
img {
  vertical-align: middle;
}
.slideshow_container {
  position: relative;
  margin: auto;
}
.prev,
.next {
  cursor: pointer;
  position: absolute;
  top: 50%;
  color: white;
  background-color: grey;
  font-weight: bold;
  transition: 0.6s ease;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  user-select: none;
  height: 40px;
  width: 40px;
  text-align: center;
  line-height: 33px;
  font-size: 40px;
  padding: 3px 5px 3px 1px;
}
.next {
  right: 0;
  border-radius: unset;
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
  padding: 3px 1px 3px 5px;
}
.prev:hover,
.next:hover {
  background-color: rgba(0, 0, 0, 0.8);
}
.dotdot {
  cursor: pointer;
  height: 10px;
  width: 10px;
  margin: 0 2px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
  transition: background-color 0.6s ease;
}
.active,
.dot:hover {
  background-color: #717171;
}
.fade {
  -webkit-animation-name: fade;
  -webkit-animation-duration: 1.5s;
  animation-name: fade;
  animation-duration: 1.5s;
}
@-webkit-keyframes fade {
  from {
    opacity: 0.4;
  }
  to {
    opacity: 1;
  }
}
@keyframes fade {
  from {
    opacity: 0.4;
  }
  to {
    opacity: 1;
  }
}
@media only screen and (max-width: 300px) {
  .prev,
  .next,
  .text {
    font-size: 11px;
  }
}

@media screen and (max-width: 600px) {
  .home_card_footer_director {
    display: block;
    flex: unset;
    padding-bottom: 0px;
  }
  .home_card_footer_btns {
    height: 35px;
  }
  .home_card_footer_btns:hover::after {
    display: none;
  }
  .home_card_like {
    float: none;
    display: inline-block;
    height: 100%;
  }
  .home_card_like_cnt {
    display: inline-block;
    font-size: 14px;
    transform: translate(5px, -3px);
  }
}
</style>
