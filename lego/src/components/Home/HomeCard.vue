<template>
  <div class="home-card-body">
    <div class="home-card-header">
      Title
    </div>
    <div class="home-card-imgs">
      <div class="slideshow-container">
        <div
          class="go-detail-btn"
          @click="goDetail()"
          :style="styleFlag ? matrixStyle[4] : instaStyle[4]"
        >
          상세보기
        </div>
        <div :class="`mySlides${idx} fade`">
          <img
            src="../../assets/git.png"
            :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
          />
        </div>

        <div :class="`mySlides${idx} fade`">
          <img
            src="../../assets/logo.png"
            :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
          />
        </div>

        <div :class="`mySlides${idx} fade`">
          <img
            src="../../assets/JS.png"
            :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
          />
        </div>

        <div :class="`mySlides${idx} fade`">
          <img
            src="../../assets/logo.png"
            :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
          />
        </div>

        <div :class="`mySlides${idx} fade`">
          <img
            src="../../assets/side_bg.png"
            :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
          />
        </div>

        <div :class="`mySlides${idx} fade`">
          <img
            src="../../assets/JS.png"
            style="width:100%"
            :style="styleFlag ? matrixStyle[3] : instaStyle[3]"
          />
        </div>

        <a class="prev" @click.stop="plusSlides(-1)">&#10094;</a>
        <a class="next" @click.stop="plusSlides(1)">&#10095;</a>
      </div>
    </div>
    <div
      class="home-card-footer"
      :style="styleFlag ? matrixStyle[1] : instaStyle[1]"
    >
      <div :style="styleFlag ? matrixStyle[0] : instaStyle[0]">
        <span :class="`dot${idx}`" @click="currentSlide(1)"></span>
        <span :class="`dot${idx}`" @click="currentSlide(2)"></span>
        <span :class="`dot${idx}`" @click="currentSlide(3)"></span>
        <span :class="`dot${idx}`" @click="currentSlide(4)"></span>
        <span :class="`dot${idx}`" @click="currentSlide(5)"></span>
        <span :class="`dot${idx}`" @click="currentSlide(6)"></span>
      </div>
      <div :style="styleFlag ? matrixStyle[2] : instaStyle[2]">
        <div class="home-card-footer-director">
          Director. Nalbo_Nalbo
        </div>
        <div class="home-card-footer-btns">
          <button v-if="like" class="home-card-like" @click="pushLike()">
            <i class="fas fa-heart" />
          </button>
          <button v-else class="home-card-like" @click="pushLike()">
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
    }
  },
  data() {
    return {
      like: false,
      slideIndex: 1,
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
    goDetail() {
      router.push("/detail");
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
.home-card-body {
  text-align: initial;
}
.home-card-header {
  padding: 10px;
}
.home-card-imgs {
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
.home-card-footer-director {
  padding: 5px;
  flex: 1;
}
.home-card-like {
  color: red;
  font-size: 25px;
  float: right;
}
.go-detail-btn {
  position: absolute;
  cursor: pointer;
  background-color: rgba(255, 215, 0, 0.5);
  color: black;
  font-weight: 700;
  padding: 5px;
  text-align: center;
  z-index: 10;
}
.mySlides {
  display: none;
}
img {
  vertical-align: middle;
}
.slideshow-container {
  /* max-width: 1000px; */
  position: relative;
  margin: auto;
  /* height: 614px; */
  /* overflow: hidden;
  box-sizing: content-box; */
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
