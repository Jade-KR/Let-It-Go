<template>
  <div class="container">
    <div v-if="imgFlag === true">
      <div>
        <div v-for="(url, i) in imageList" :key="`url-${i}`">
          <div class="mySlides">
            <img
              :src="url"
              class="detail-imgs"
              v-if="images"
              @error="imgError"
            />
            <img
              src="../../../assets/icons/no_img.jpg"
              alt="no_images"
              class="detail-imgs"
              v-else
            />
          </div>
        </div>

        <a class="prev" @click="plusSlides(-1)" v-if="images">❮</a>
        <a class="next" @click="plusSlides(1)" v-if="images">❯</a>
      </div>
      <div class="row">
        <div
          class="column"
          v-for="(url, i) in imageList"
          :key="`thumnail-${i}`"
        >
          <img
            class="demo cursor"
            :src="url"
            @click="currentSlide(i + 1)"
            v-if="images"
          />
        </div>
      </div>
    </div>

    <div v-else>
      <div>
        <img
          src="../../../assets/icons/no_img.jpg"
          alt="no_images"
          class="detail-imgs"
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
      slideIndex: 1,
      imageList: ["images/icons/no_img.jpg"],
      imgFlag: true
    };
  },
  mounted() {
    if (this.images) {
      this.imageList = this.images.split("|");
    }
    this.showSlides(this.slideIndex);
  },
  methods: {
    imgError() {
      this.imgFlag = false;
    },
    plusSlides(n) {
      this.showSlides((this.slideIndex += n));
    },

    currentSlide(n) {
      this.showSlides((this.slideIndex = n));
    },

    showSlides(n) {
      var i;
      var slides = document.getElementsByClassName("mySlides");
      if (this.images) {
        var dots = document.getElementsByClassName("demo");
      }
      if (n > slides.length) {
        this.slideIndex = 1;
      }
      if (n < 1) {
        this.slideIndex = slides.length;
      }
      for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
      }
      if (this.images) {
        for (i = 0; i < dots.length; i++) {
          dots[i].className = dots[i].className.replace(" active", "");
        }
        dots[this.slideIndex - 1].className += " active";
      }
      slides[this.slideIndex - 1].style.display = "block";
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
@media screen and (max-width: 600px) {
  .mySlides {
    height: 100vw;
  }
  .row {
    width: 100%;
    margin: 5px 0;
  }
  .column {
    height: 100%;
  }
  .demo {
    width: 16.6vw;
    height: 16.6vw;
  }
}
</style>
