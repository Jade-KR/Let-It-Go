<template>
  <div>
    <div class="whole_box">
      <div class="my_photo">
        <div class="photo_box">
          <img
            src="https://images.unsplash.com/photo-1472457974886-0ebcd59440cc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60"
            alt="photo"
          />
        </div>
      </div>
      <div class="my_info">
        <div class="info_top">
          <span class="user_id">Jade</span>
          <UserModal>
            <span class="user_setting" slot="click">
              <i class="fas fa-cog"></i>
            </span>
          </UserModal>
        </div>
        <div class="info_middle">
          <div v-for="i in summaryItems.length" :key="i" class="summary">
            <span>{{ summaryItems[i - 1].title }} {{summaryItems[i - 1].cnt}}</span>
          </div>
        </div>
        <div class="info_bottom">{{ comment }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import UserModal from "./UserModal";
export default {
  components: {
    UserModal
  },
  data() {
    return {
      summaryItems: [
        { title: "설계도", cnt: "0" },
        { title: "팔로우", cnt: "0" },
        { title: "팔로잉", cnt: "0" }
      ],
      comment:
        "새로운 회계연도가 개시될 때까지 예산안이 의결되지 못한 때에는 정부는 국회에서 예산안이 의결될 때까지 다음의 목적을 위한 경비는 전년도 예산에 준하여 집행할 수 있다.연소자의 근로는 특별한 보호를 받는다. 체포·구속·압수 또는 수색을 할 때에는 적법한 절차에 따라 검사의 신청에 의하여 법관이 발부한 영장을 제시하여야 한다. 다만, 현행범인인 경우와 장기 3년 이상의 형에 해당하는 죄를 범하고 도피 또는 증거인멸의 염려가 있을 때에는 사후에 영장을 청구할 수 있다",
      dialog: false
    };
  },
  methods: {}
};
</script>

<style scoped>
.whole_box {
  display: flex;
  flex-flow: row nowrap;
  border-style: none;
  width: 100%;
  height: 200px;
  margin-top: 30px;
}
.my_photo {
  border-style: none;
  height: 100%;
  width: 30%;
  margin-right: 30px;
}
.my_info {
  border-style: none;
  width: 70%;
  height: fit-content;
}
.info_top {
  border-style: none;
  height: auto;
  margin-bottom: 20px;
  display: flex;
  align-items: baseline;
}
.info_middle {
  display: flex;
  border-style: none;
  height: auto;
  margin-bottom: 20px;
}
.info_bottom {
  border-style: none;
  height: 100px;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}
.photo_box {
  border-style: none;
  height: 90%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.photo_box > img {
  width: 70%;
  height: 100%;
  border-radius: 180%;
}
.user_id {
  font-size: 30px;
  margin-right: 10px;
}
.summary {
  margin-right: 20px;
}
.user_setting:hover {
  cursor: pointer;
}
.user_setting > i {
  font-size: 25px;
}
</style>