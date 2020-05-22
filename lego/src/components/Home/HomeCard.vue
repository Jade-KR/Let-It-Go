<template>
  <div class="home_card_body">
    <div class="home_card_header">
      {{ name }}
    </div>
    <div class="home_card_imgs">
      <div class="slideshow_container">
        <div
          class="go_detail_btn"
          @click="goDetail(id)"
          :style="styleFlag ? matrixStyle[4] : instaStyle[4]"
        >
          상세보기
        </div>

        <div :class="`mySlides${idx} fade`">
          <img
            :src="images"
            alt=""
            :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
          />
        </div>

        <!-- <div v-for="(url, i) in params" :key="`url-${i}`">
          <div :class="`mySlides${idx} fade`" :id="`mySlide-${i}`">
            <img
              :src="url"
              :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
              :id="`slideImg-${i}-${idx}`"
              v-if="!images"
            />
            <img
              :src="images"
              alt=""
              :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
              :id="`slideImg-${i}-${idx}`"
              v-else
            />
          </div>
        </div> -->

        <a class="prev" @click.stop="plusSlides(-1)">&#10094;</a>
        <a class="next" @click.stop="plusSlides(1)">&#10095;</a>
      </div>
    </div>
    <div
      class="home_card_footer"
      :style="styleFlag ? matrixStyle[1] : instaStyle[1]"
    >
      <div :style="styleFlag ? matrixStyle[0] : instaStyle[0]">
        <span
          :class="`dot${idx}`"
          @click="currentSlide(1)"
          v-if="params.length >= 1"
        ></span>
        <span
          :class="`dot${idx}`"
          @click="currentSlide(2)"
          v-if="params.length >= 2"
        ></span>
        <span
          :class="`dot${idx}`"
          @click="currentSlide(3)"
          v-if="params.length >= 3"
        ></span>
        <span
          :class="`dot${idx}`"
          @click="currentSlide(4)"
          v-if="params.length >= 4"
        ></span>
        <span
          :class="`dot${idx}`"
          @click="currentSlide(5)"
          v-if="params.length >= 5"
        ></span>
        <span
          :class="`dot${idx}`"
          @click="currentSlide(6)"
          v-if="params.length >= 6"
        ></span>
      </div>
      <div :style="styleFlag ? matrixStyle[2] : instaStyle[2]">
        <div class="home_card_footer_director">Director. {{ nickname }}</div>
        <div class="home_card_footer_btns">
          <button v-if="like" class="home_card_like" @click="pushLike()">
            <i class="fas fa-heart" />
          </button>
          <button v-else class="home_card_like" @click="pushLike()">
            <i class="far fa-heart" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router";

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
    }
  },
  data() {
    return {
      like: false,
      slideIndex: 1,
      params: [
        "/images/로고2.png",
        "/images/side_bg.png",
        "/images/부품들.jpg",
        "/images/git.png",
        "/images/header.jpg",
        "/images/login_bg.jpg"
      ],
      matrixStyle: [
        {
          display: "block",
          textAlign: "center"
        },
        {
          padding: "5px",
          display: "block"
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
        }
      ],
      instaStyle: [
        {
          position: "absolute",
          right: "50%",
          transform: "translateX(50%)"
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
          // maxHeight: "800px"
        },
        {
          left: "87.7%"
        }
      ]
    };
  },
  mounted() {
    var i;
    var n = 1;
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
  },
  methods: {
    test() {
      var maxHeight = 0;
      for (let i = 0; i < this.params.length; ++i) {
        var naturalHeight = document.getElementById(`slideImg-${i}-${this.idx}`)
          .naturalHeight; // img 높이
        if (maxHeight < naturalHeight) {
          maxHeight = naturalHeight;
        }
      }
      if (maxHeight > 614) {
        maxHeight = 614;
      }
      for (let i = 0; i < this.params.length; ++i) {
        document.getElementById(`slideImg-${i}-${this.idx}`).style.height =
          String(maxHeight) + "px";
      }
    },
    goDetail() {
      router.push("/detail" + "/" + this.id);
    },
    pushLike() {
      if (this.like === false) {
        this.like = true;
      } else {
        this.like = false;
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
}
.home_card_imgs {
  border-top: 5px solid gold;
  border-bottom: 5px solid gold;
}
/* .home-card-img {
  height: 100%;
  width: 100%;
} */
/* .home-card-footer {
  padding: 10px;
  display: flex;
} */
.home_card_footer_director {
  padding: 5px;
  flex: 1;
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
  border-radius: 50%;
  user-select: none;
  height: 25px;
  width: 25px;
  text-align: center;
  font-size: 14px;
  padding: 3px;
}
.next {
  right: 0;
  border-radius: 50%;
}
.prev:hover,
.next:hover {
  background-color: rgba(0, 0, 0, 0.8);
}
.dot1,
.dot2,
.dot3,
.dot4,
.dot5,
.dot6,
.dot7,
.dot8,
.dot9,
.dot10 {
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
</style>
