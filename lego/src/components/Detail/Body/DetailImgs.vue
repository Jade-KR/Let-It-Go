<template>
  <div class="container">
    <div>
      <div class="mySlides">
        <img src="../../../assets/git.png" class="detail-imgs" />
      </div>

      <div class="mySlides">
        <img src="../../../assets/JS.png" class="detail-imgs" />
      </div>

      <div class="mySlides">
        <img src="../../../assets/logo.png" class="detail-imgs" />
      </div>

      <div class="mySlides">
        <img src="../../../assets/side_bg.png" class="detail-imgs" />
      </div>

      <a class="prev" @click="plusSlides(-1)">❮</a>
      <a class="next" @click="plusSlides(1)">❯</a>
    </div>
    <div class="row">
      <div class="column">
        <img
          class="demo cursor"
          src="../../../assets/git.png"
          @click="currentSlide(1)"
        />
      </div>
      <div class="column">
        <img
          class="demo cursor"
          src="../../../assets/JS.png"
          @click="currentSlide(2)"
        />
      </div>
      <div class="column">
        <img
          class="demo cursor"
          src="../../../assets/logo.png"
          @click="currentSlide(3)"
        />
      </div>
      <div class="column">
        <img
          class="demo cursor"
          src="../../../assets/side_bg.png"
          @click="currentSlide(4)"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    images: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      slideIndex: 1
    };
  },
  mounted() {
    this.showSlides(this.slideIndex);
  },
  methods: {
    plusSlides(n) {
      this.showSlides((this.slideIndex += n));
    },

    currentSlide(n) {
      this.showSlides((this.slideIndex = n));
    },

    showSlides(n) {
      var i;
      var slides = document.getElementsByClassName("mySlides");
      var dots = document.getElementsByClassName("demo");
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
img {
  vertical-align: middle;
}
.container {
  position: relative;
  padding: 0px;
}
.mySlides {
  display: none;
  height: 700px;
  overflow: hidden;
}
.detail-imgs {
  width: 100%;
  height: 100%;
}
.cursor {
  cursor: pointer;
}
.prev,
.next {
  cursor: pointer;
  position: absolute;
  top: 40%;
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
.row {
  justify-content: center;
  margin-top: 10px;
}
.row:after {
  content: "";
  display: table;
  clear: both;
}
.column {
  width: 16.66%;
  height: 100px;
}
.demo {
  opacity: 0.6;
  width: 100%;
  height: 100%;
}
.active,
.demo:hover {
  opacity: 1;
}
</style>
