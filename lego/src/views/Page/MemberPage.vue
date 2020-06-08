<template>
  <div>
    <div v-if="isSkip === false" id="intro_box">
      <div id="intro_skip" @click="skip()">
        SKIP
      </div>
      <video autoplay controls width="80%">
        <source src="../../assets/Intro.mp4" type="video/mp4" />
      </video>
    </div>
    <section v-else>
      <div class="slide">
        <div class="content">
          <h2>김평강</h2>
          <p>Back End (추천, AI, IoT, RESTful API, 배포)</p>
          <p>특징 (프로젝트 총괄, AI, Big Data, IoT 관심많음)</p>
          <p>기타 (어디로 가야하나..)</p>
        </div>
      </div>
      <div class="slide">
        <div class="content">
          <h2>김사덕</h2>
          <p>Back-End (추천, Recognition, 발표)</p>
          <p>특징 (원래확찐자)</p>
          <p>기타 (싸피 마무리 잘하자)</p>
        </div>
      </div>
      <div class="slide">
        <div class="content">
          <h2>김정덕</h2>
          <p>Front-End (MyPage, UserSetting, LegoRail, UCC)</p>
          <p>특징 (새로운 보금자리 찾는 중)</p>
          <p>기타 (1년 빠르구나..)</p>
        </div>
      </div>
      <div class="slide">
        <div class="content">
          <h2>윤명훈</h2>
          <p>Back-End (DB모델링, 인증 및 권한 관련 API)</p>
          <p>IoT (컨베이어 벨트 제작 및 보완)</p>
          <p>AI (Object Detection, 학습이미지 생성)</p>
          <p>특징 (여름 싫어함)</p>
          <p>기타 (코로나 조심합시다..ㅠ)</p>
        </div>
      </div>
      <div class="slide">
        <div class="content">
          <h2>이지훈</h2>
          <p>
            Front-End (Home, Search, Write, Detail, Login, Register, Admin,
            BugFix, Mobile)
          </p>
          <p>특징 (확진짜아주확찐자매우확찐자)</p>
          <p>기타 (코로나Out)</p>
        </div>
      </div>
      <div class="slide">
        <div class="content">
          <div id="side">
            LE
            <div id="inner">
              t it
            </div>
            GO
          </div>
          <br />
          <a id="goAdmin" href="https://lab.ssafy.com/s02-final/s02p31d108">
            Go Git Lab</a
          >
          <p id="goHome" @click="goHome()">돌아가기</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { mapMutations } from "vuex";
import router from "../../router";

export default {
  data() {
    return {
      isSkip: false
    };
  },
  async mounted() {
    this.setAuthFlag(true);
    setTimeout(() => {
      this.isSkip = true;
    }, 43200);
  },
  destroyed() {
    this.setAuthFlag(false);
  },
  methods: {
    ...mapMutations("auth", ["setAuthFlag"]),
    goHome() {
      this.setAuthFlag(false);
      router.push("/");
    },
    skip() {
      this.isSkip = true;
    }
  }
};
</script>

<style scoped>
#intro_box {
  text-align: center;
  background-color: black;
  padding: 40px;
}
#intro_skip {
  position: absolute;
  color: white;
  border: 3px solid white;
  width: 100px;
  padding: 10px;
  right: 50px;
  top: 40px;
  cursor: pointer;
}
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
#side {
  display: inline-block;
  font-size: 30px;
  font-weight: 700;
  color: gold;
  letter-spacing: 0.1px;
}
#inner {
  display: inline-block;
  font-size: 18px;
  letter-spacing: 0.1px;
}
</style>
