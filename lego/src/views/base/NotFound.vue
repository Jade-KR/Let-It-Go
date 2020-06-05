<template>
  <div id="notfound_back">
    <div id="notfound_box">
      <div id="notfound_badgate">
        잘못된 접근입니다
      </div>
      <div id="notfound_gohome" @click="goHome()">
        홈으로 돌아가기
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router";
import { mapMutations } from "vuex";

export default {
  mounted() {
    this.setAuthFlag(true);
  },
  destroyed() {
    this.setAuthFlag(false);
  },
  methods: {
    ...mapMutations("auth", ["setAuthFlag"]),
    goHome() {
      router.push("/");
    }
  }
};
</script>

<style scoped>
#notfound_back {
  text-align: center;
  height: 100%;
  background-color: white;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
#notfound_box {
  border: 5px solid;
  color: gold;
  width: 50vw;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 30px;
}
#notfound_badgate {
  color: gold;
  font-size: 60px;
  font-weight: 500;
  letter-spacing: 8px;
  margin-bottom: 20px;
  background: white;
  position: relative;
  animation: text 3s 1;
}
#notfound_gohome {
  cursor: pointer;
  color: #6ab04c;
}

@keyframes text {
  0% {
    color: white;
    margin-bottom: -40px;
  }
  30% {
    letter-spacing: 25px;
    margin-bottom: -40px;
  }
  85% {
    letter-spacing: 8px;
    margin-bottom: -40px;
  }
}
@media screen and (max-width: 600px) {
  #notfound_box {
    width: 80vw;
    height: 90%;
  }
  #notfound_badgate {
    font-size: 60px;
    letter-spacing: 8px;
    margin-top: 40vw;
  }
}
</style>
