<template>
  <div id="home-body">
    <div id="home-show">
      <div
        @click="styleCheck()"
        v-if="styleFlag === false"
        class="home-show-btn"
      >
        모아보기
      </div>
      <div v-else @click="styleCheck()" class="home-show-btn">
        크게보기
      </div>
    </div>
    <div :style="styleFlag ? matrixWidth : instaWidth">
      <div
        class="home-card"
        v-for="i in 5"
        :key="i"
        :style="styleFlag ? matrixStyle : instaStyle"
      >
        <home-card :idx="i" :styleFlag="styleFlag" />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HomeCard from "@/components/Home/HomeCard";

export default {
  name: "Home",
  components: {
    HomeCard
  },
  data() {
    return {
      styleFlag: false,
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
      }
    };
  },
  methods: {
    styleCheck() {
      if (this.styleFlag === false) {
        this.styleFlag = true;
      } else {
        this.styleFlag = false;
      }
    }
  }
};
</script>

<style scoped>
#home-body {
  /* border: 1px solid black; */
  box-sizing: border-box;
  position: absolute;
  top: 100px;
  width: 100%;
  background-color: rgb(245, 245, 245);
}
#home-show {
  width: 120px;
  padding: 10px;
  text-align: center;
  position: sticky;
  top: 20px;
  float: right;
  /* right: 10vw; */
}
.home-show-btn {
  cursor: pointer;
  background-color: skyblue;
  line-height: 50px;
  color: white;
  font-weight: 600;
  font-size: 20px;
}
</style>
