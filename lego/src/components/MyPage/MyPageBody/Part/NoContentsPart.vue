<template>
  <div>
    <div class="no_content_box">
      <h2 class="no_content_header">보유하고 있는 부품이 없습니다</h2>
      <br />
      <div class="no_content_body" v-if="check === true">
        <div class="no_content_body_left">
          <p class="no_content_contents">레고 마스터에서</p>
          <p class="no_content_contents">분류된 부품들 추가하기</p>
          <i class="fas fa-angle-double-down no_content_icons"></i>
          <button class="no_content_btn" @click.prevent="goLegoRail()">
            GO Lego Rail!
          </button>
        </div>
        <div class="no_content_body_right">
          <p class="no_content_contents">직접</p>
          <p class="no_content_contents">부품 추가하기</p>
          <i class="fas fa-angle-double-down no_content_icons"></i>
          <AddParts @close="added">
            <button class="no_content_btn" slot="click">ADD Parts!</button>
          </AddParts>
        </div>
      </div>
      <div v-else></div>
    </div>
  </div>
</template>

<script>
import AddParts from "./AddParts/AddParts";
export default {
  components: {
    AddParts
  },
  data() {
    return {
      check: ""
    };
  },
  mounted() {
    this.$route.params.user_id === localStorage.getItem("pk")
      ? (this.check = true)
      : (this.check = false);
  },
  methods: {
    goLegoRail() {
      this.$router.push({
        name: "UserSetting",
        params: { title: "레고레일", idx: 2 }
      });
    },
    added() {
      this.$emit("added");
    }
  }
};
</script>

<style scoped>
.no_content_box {
  border: rgb(255, 222, 162) solid 2px;
  width: 90%;
  margin: auto;
  margin-bottom: 100px;
}
.no_content_header {
  text-align: center;
  width: fit-content;
  margin: 10px auto;
  border-bottom: rgb(255, 194, 80) 2px dotted;
}
.no_content_body {
  border-top: solid rgb(255, 209, 124) 1px;
  width: 90%;
  margin: auto;
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}
.no_content_body_left {
  border-right: solid rgb(255, 209, 124) 2px;
  display: flex;
  flex-flow: column;
  align-items: center;
  width: 100%;
  margin-top: 10px;
}
.no_content_body_right {
  display: flex;
  flex-flow: column;
  align-items: center;
  width: 100%;
  margin-top: 10px;
}
.no_content_contents {
  color: rgb(165, 165, 165);
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}
.no_content_btn {
  width: fit-content;
  font-size: 20px;
  border: 1px solid rgb(255, 209, 124);
  padding: 0px 10px;
  height: fit-content;
  margin-top: 10px;
  transition: ease-in-out 0.3s all;
  -webkit-animation: blink 1s 1s 3 linear normal;
  -moz-animation: blink 1s 1s 3 linear normal;
  -ms-animation: blink 1s 1s 3 linear normal;
  -o-animation: blink 1s 1s 3 linear normal;
  animation: blink 1s 1s 3 linear normal;
}
.no_content_btn:hover {
  background: orange;
}
.no_content_icons {
  font-size: 30px;
  margin: 10px 0;
  -webkit-animation: down 1s 1s 3 linear normal;
  -moz-animation: down 1s 1s 3 linear normal;
  -ms-animation: down 1s 1s 3 linear normal;
  -o-animation: down 1s 1s 3 linear normal;
  animation: down 1s 1s 3 linear normal;
}
@keyframes blink {
  from {
    background: white;
  }
  to {
    background: orange;
  }
}
@keyframes down {
  from {
    transform: translateY(0px);
  }
  to {
    transform: translateY(16px);
  }
}
</style>
