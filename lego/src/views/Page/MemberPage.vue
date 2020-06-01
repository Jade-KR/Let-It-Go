<template>
  <div>
    <!-- <div v-if="admin == true">
      <adminDetail />
    </div>
    <div v-else> -->
    <section v-if="main">
      <div class="slide">
        <div class="content">
          <h2>김평강</h2>
          <p>Back End (REST API, 배포, 알고리즘 최적화, SVDPP)</p>
          <p>특징 (프로젝트 총괄, 스마트팩토리 관심많음)</p>
          <p>기타 (취직하고싶다..)</p>
        </div>
      </div>
      <div class="slide">
        <div class="content">
          <h2>김사덕</h2>
          <p>
            Back End (추천 시스템, 보고서 컨텐츠 기획 및 데이터 분석, K-Means,
            KNN)
          </p>
          <p>특징 (싸피 출근하고 싶어함)</p>
          <p>기타 (데이터 분석 하고 싶음)</p>
        </div>
      </div>
      <div class="slide">
        <div class="content">
          <h2>김정덕</h2>
          <p>Front End (SearchPage, StoreDetail, Location Based, Word Cloud)</p>
          <p>Back End (TF-IDF)</p>
          <p>특징(프론트 총괄, UCC, 글로벌 글로벌, 타이완 넘버 원)</p>
          <p>기타(지훈이형.. 2달은 우습지 ㅎㅎ)</p>
        </div>
      </div>
      <div class="slide">
        <div class="content">
          <h2>윤명훈</h2>
          <p>Back End(인증 및 권한, 보고서 컨텐츠 기획 및 데이터 분석)</p>
          <p>특징(young함)</p>
          <p>기타(형들 말 잘들음)</p>
        </div>
      </div>
      <div class="slide">
        <div class="content">
          <h2>이지훈</h2>
          <p>
            Front-End (Home, Search, Write, Login, Register)
          </p>
          <p>특징 (확진짜아주확찐자매우확찐자, 하리보고양이)</p>
          <p>기타 (코로나Out)</p>
        </div>
      </div>
      <div class="slide">
        <div class="content">
          <h2>LEt it GO</h2>
          <a id="goAdmin" href="https://lab.ssafy.com/s02-final/s02p31d108">
            Go Git Lab</a
          >
          <p id="goHome" @click="goHome()">돌아가기</p>
        </div>
      </div>
    </section>
    <!-- <div v-if="before" id="before">
      빠져든다ㅏㅏㅏㅏㅏㅏㅏㅏㅏ
    </div>
    <div v-if="timeOut" id="admin_main">
      <div class="scene">
        <div class="wrap">
          <div class="wall wall-right" />
          <div class="wall wall-left" />
          <div class="wall wall-top" />
          <div class="wall wall-bottom" />
          <div class="wall wall-back" />
        </div>
        <div class="wrap">
          <div class="wall wall-right" />
          <div class="wall wall-left" />
          <div class="wall wall-top" />
          <div class="wall wall-bottom" />
          <div class="wall wall-back" />
        </div>
      </div>
    </div> -->
    <!-- </div> -->
  </div>
</template>

<script>
import { mapMutations } from "vuex";
import router from "../../router";

export default {
  data() {
    return {
      // timeOut: false,
      // before: true,
      // main: false
      main: true
    };
  },
  async mounted() {
    this.setAuthFlag(true);

    // setTimeout(() => {
    //   this.timeOut = true;
    //   this.before = false;
    // }, 2000);
    // setTimeout(() => {
    //   this.timeOut = false;
    //   this.main = true;
    // }, 6000);
  },
  destroyed() {
    this.setAuthFlag(false);
  },
  methods: {
    ...mapMutations("auth", ["setAuthFlag"]),
    goHome() {
      this.setAuthFlag(false);
      router.push("/");
    }
    // goAdmin() {
    //   this.admin = true
    // }
  }
};
</script>

<style scoped>
#goAdmin {
  cursor: pointer;
  text-decoration: none;
  color: white;
  font-size: 20px;
}
#goHome {
  cursor: pointer;
}
#before {
  font-size: 200px;
  font-weight: 500;
  text-align: center;
}
#test {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
section {
  position: absolute;
  width: 100%;
  height: 100vh;
  display: flex;
  border: 2px solid black;
}
section .slide {
  position: relative;
  /* background-color: green; */
  height: 100%;
  flex: 1;
  border-right: 2px solid black;
  overflow: hidden;
  transition: 0.5s ease-in-out;
}
section .slide:last-child {
  border-right: none;
}
section .slide:hover {
  flex-grow: 5;
}
section .slide:nth-child(1) {
  background-image: url("../../../public/images/member/KPG.jpg");
  background-size: cover;
  background-position: center center;
}
section .slide:nth-child(2) {
  background-image: url("../../../public/images/member/KSD.jpg");
  background-size: cover;
  background-position: center center;
}
section .slide:nth-child(3) {
  background-image: url("../../../public/images/member/KJD3.jpg");
  background-size: cover;
  background-position: center center;
}
section .slide:nth-child(4) {
  background-image: url("../../../public/images/member/YMH.jpg");
  background-size: cover;
  background-position: center center;
}
section .slide:nth-child(5) {
  background-image: url("../../../public/images/member/LJH.jpg");
  background-size: cover;
  background-position: center center;
}
section .slide:nth-child(6) {
  background-image: url("../../../public/images/logo.png");
  background-size: contain;
  background-position: center center;
}
section .slide .content {
  position: absolute;
  bottom: 0;
  margin: 40px;
  padding: 30px;
  background-color: black;
  color: white;
  visibility: hidden;
  opacity: 0;
  transition: 0.5s;
  /* transform: translateY(50px); */
}
section .slide:hover .content {
  visibility: visible;
  opacity: 1;
  transition: 0.5s;
  transition-delay: 0.5s;
  /* transform: translateY(50px); */
}
section .slide .content h2 {
  margin-bottom: 10px;
}
.wall {
  background: url(https://s3-us-west-2.amazonaws.com/s.cdpn.io/18515/PIA09959-1280x800_copy.jpg);
  background-size: cover;
}
#admin_main {
  height: 100vh;
  width: 100%;
  overflow: hidden;
  background: #000;
  text-align: center;
}
#admin_main:before {
  content: "";
  display: inline-block;
  height: 40%;
  vertical-align: middle;
}
.scene {
  display: inline-block;
  vertical-align: middle;
  perspective: 5px;
  perspective-origin: 50% 50%;
  position: relative;
}

.wrap {
  position: absolute;
  width: 1000px;
  height: 1000px;
  left: -500px;
  top: -500px;
  transform-style: preserve-3d;
  animation: move 12s infinite linear;
  animation-fill-mode: forwards;
}

.wrap:nth-child(2) {
  animation: move 12s infinite linear;
  animation-delay: 6s;
}

.wall {
  width: 100%;
  height: 100%;
  position: absolute;
  opacity: 0;
  animation: fade 12s infinite linear;
  animation-delay: 0;
}

.wrap:nth-child(2) .wall {
  animation-delay: 6s;
}

.wall-right {
  transform: rotateY(90deg) translateZ(500px);
}

.wall-left {
  transform: rotateY(-90deg) translateZ(500px);
}

.wall-top {
  transform: rotateX(90deg) translateZ(500px);
}

.wall-bottom {
  transform: rotateX(-90deg) translateZ(500px);
}

.wall-back {
  transform: rotateX(180deg) translateZ(500px);
}

@keyframes move {
  0% {
    transform: translateZ(-500px) rotate(0deg);
  }
  100% {
    transform: translateZ(500px) rotate(0deg);
  }
}

@keyframes fade {
  0% {
    opacity: 0;
  }
  25% {
    opacity: 1;
  }
  75% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>
