<template>
  <div>
    <div>
      <div class="container">
        <div>
          <div v-for="(img, i) in modelImgs" :key="`img-${i}`">
            <div class="mySlides" :id="`myslide-${i}`">
              <img :src="img" class="detail-imgs" />
            </div>
          </div>

          <a id="prev" @click="plusSlides(-1)">❮</a>
          <a id="next" @click="plusSlides(1)">❯</a>
        </div>
        <div class="row">
          <div class="column" v-for="(img, i) in modelImgs" :key="`thumbnail-${i}`">
            <img class="demo cursor" :src="img" @click="currentSlide(i + 1)" :id="`thumbnail-${i}`" />
            <div class="delete_btn" @click="removeImage(i)">삭제</div>
          </div>
        </div>
      </div>
      <div class="filebox">
        <label for="ex_filename">사진선택</label>
        <input
          type="file"
          id="ex_filename"
          class="upload-hidden"
          multiple="multiple"
          @change="onFileChange"
        />
      </div>
    </div>
    <div>
      <button @click="onPrev(step - 1)" class="before_btn">이전</button>
      <button @click="onNext(step + 1)" :disabled="modelImgs.length === 0" class="after_btn">다음</button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations } from "vuex";

export default {
  data() {
    return {
      files: "",
      slideIndex: 1
    };
  },
  computed: {
    ...mapState({
      model: state => state.write.model,
      step: state => state.write.step,
      currentStep: state => state.write.currentStep,
      modelImgs: state => state.write.modelImgs
    })
  },
  watch: {
    modelImgs() {
      if (this.modelImgs.length === 0) {
        const prev = document.getElementById("prev");
        const next = document.getElementById("next");
        prev.style.display = "none";
        next.style.display = "none";
      }
    }
  },
  mounted() {
    if (this.modelImgs.length > 0) {
      const prev = document.getElementById("prev");
      const next = document.getElementById("next");
      prev.style.display = "block";
      next.style.display = "block";
    }
  },
  methods: {
    ...mapActions("write", ["next", "prev", "removeImg"]),
    ...mapMutations("write", ["setSteps", "setCurrentStep"]),
    goStep(idx) {
      if (this.currentStep >= idx || this.step >= idx) {
        this.setCurrentStep(idx);
      }
    },
    onStep(idx) {
      this.setStep(idx);
    },
    onNext(idx) {
      const params = {
        idx: idx,
        step: 1
      };
      this.next(params);
    },
    onPrev(idx) {
      const params = {
        idx: idx,
        step: 1
      };
      this.prev(params);
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
    },

    onFileChange(e) {
      this.files = e.target.files || e.dataTransfer.files;
      if (!this.files.length) {
        return;
      }
      if (
        this.files.length > 6 ||
        this.modelImgs.length + this.files.length > 6
      ) {
        alert("사진은 최대 6장까지 가능합니다.");
        return;
      }
      for (let i = 0; i < this.files.length; ++i) {
        this.createImage(this.files[i]);
      }
      const prev = document.getElementById("prev");
      const next = document.getElementById("next");
      prev.style.display = "block";
      next.style.display = "block";
    },
    createImage(file) {
      var reader = new FileReader();
      var vm = this;
      reader.onload = e => {
        for (let i = 0; i < vm.modelImgs.length; ++i) {
          if (vm.modelImgs[i] === e.target.result) {
            alert("중복되는 사진이 있습니다.");
            return;
          }
        }
        vm.modelImgs.push(e.target.result);
      };
      reader.readAsDataURL(file);
    },
    removeImage(idx) {
      const temp = [];
      for (let i = 0; i < this.files.length; ++i) {
        if (i !== idx) {
          temp.push(this.files[i]);
        }
      }
      this.files = temp;
      const params = {
        idx: idx,
        files: this.files
      };
      this.removeImg(params);
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
  display: flex;
}
.mySlides {
  display: none;
  height: 100%;
  overflow: hidden;
  border: 1px solid gold;
}
#myslide-0 {
  display: block;
}
.detail-imgs {
  width: 600px;
  height: 600px;
}
.cursor {
  cursor: pointer;
}
#prev,
#next {
  display: none;
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
#next {
  right: 205px;
  border-radius: 50%;
}
#prev:hover,
#next:hover {
  background-color: rgba(0, 0, 0, 0.8);
}
.row {
  margin-left: 10px;
}
.column {
  display: flex;
}
.demo {
  opacity: 0.6;
  width: 200px;
  height: 100px;
}
.active,
.demo:hover {
  opacity: 1;
}
.delete_btn {
  position: absolute;
  right: 0;
  background-color: rgba(255, 0, 0, 0.5);
  padding: 5px;
  cursor: pointer;
  color: white;
}
.delete_btn:hover {
  background-color: red;
}
.before_btn,
.after_btn {
  background-color: gold;
  padding: 10px;
  border-radius: 20px;
  width: 100px;
  margin-top: 20px;
}
.before_btn:hover,
.after_btn:hover {
  background-color: green;
  color: white;
}
.before_btn {
  background-color: white;
  color: white;
  cursor: default;
}
.before_btn:hover {
  background-color: white;
  color: white;
}
.after_btn {
  float: right;
}
.after_btn:disabled {
  background-color: gray;
  color: black;
}
.after_btn:disabled:hover {
  background-color: gray;
  color: black;
}

.filebox {
  margin: 20px auto 0 auto;
  text-align: center;
}
.filebox input[type="file"] {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
.filebox label {
  display: inline-block;
  padding: 0.5em 0.75em;
  font-size: inherit;
  line-height: normal;
  vertical-align: middle;
  background-color: rgba(255, 215, 0);
  color: black;
  font-size: 20px;
  cursor: pointer;
  border-radius: 0.25em;
  width: 150px;
}
.filebox label:hover {
  background-color: green;
  color: white;
}
</style>
