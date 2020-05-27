<template>
  <div
    id="model_body"
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="9"
  >
    <div class="whole_box">
      <div class="item" v-for="(item, idx) in userModels" :key="`item${idx}`">
        <div class="body_img_box">
          <img class="body_img" :src="item.images" alt />
          <div class="body_img_hover">
            <div class="body_img_info">
              <i class="fas fa-heart"></i>
              <span>0</span>
              <i class="fas fa-comment"></i>
              <span>0</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapActions, mapState } from "vuex";
export default {
  data() {
    return {
      loading: true
    };
  },
  async mounted() {
    const params = {
      page: 1,
      append: false,
      id: this.$route.params.user_id
    };
    await this.getUserModels(params);
  },
  computed: {
    ...mapState({
      userModels: state => state.mypage.userModelList,
      page: state => state.mypage.userModelPage
    })
  },
  methods: {
    ...mapActions("mypage", ["getUserModels"]),
    async loadMore() {
      this.loading = true;
      const params = {
        page: this.page,
        append: true,
        id: this.$route.params.user_id
      };

      await this.getUserModels(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    }
  }
};
</script>

<style scoped>
.whole_box {
  height: 100%;
  width: 100%;
  display: flex;
  flex-flow: row wrap;
}
.item {
  width: 260px;
  height: 250px;
  margin: 18px;
}
.body_img_box {
  width: 100%;
  height: 100%;
  background: black;
  position: relative;
}
.body_img_box > img {
  width: 100%;
  height: 100%;
  /* border-radius: 180%; */
}
.body_img_hover {
  transition: 0.5s ease;
  opacity: 0;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -90%);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
}
.body_img {
  opacity: 1;
  cursor: pointer;
  transition: 0.5s ease;
}
.body_img_box:hover .body_img {
  opacity: 0.5;
  cursor: pointer;
}
.body_img_box:hover .body_img_hover {
  opacity: 1;
  cursor: pointer;
  transform: translate(-50%, -100%);
}
.body_img_info {
  width: 100%;
  text-align: center;
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: baseline;
}
.body_img_info > i {
  font-size: 25px;
  color: white;
}
.body_img_info > span {
  margin-left: 10px;
  font-size: 25px;
  color: white;
  margin-right: 20px;
}
</style>