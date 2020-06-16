<template>
  <div>
    <div v-if="isEmpty === true">
      하위 설계도가 없습니다.
    </div>
    <div v-else style="display: inline-block; width: 100%;">
      <div
        v-for="(subSet, i) in subSets"
        :key="`subset-${i}`"
        class="item"
        @click="goDetail(subSet.id)"
      >
        <div class="body_img_box">
          <img
            class="body_img"
            src="../../../assets/icons/no_img.jpg"
            alt="no_image"
            v-if="
              subSet.images === null ||
                subSet.images === '' ||
                errorFlag === true
            "
          />
          <img
            class="body_img"
            :src="subSet.images"
            alt="image"
            v-else
            @error="imgError()"
          />

          <div class="body_img_hover">
            <div class="body_img_desc">
              <div class="body_img_name">
                <b>{{ subSet.name }}</b>
              </div>
              <div class="body_img_nick">By. {{ subSet.nickname }}</div>
              <div class="body_img_info">
                <i class="fas fa-heart"></i>
                <span>{{ subSet.likeCount }}</span>
                <i class="fas fa-comment"></i>
                <span>{{ subSet.reviewCount }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../../router";
export default {
  props: {
    subSets: {
      type: Array
    }
  },
  data() {
    return {
      isEmpty: true,
      errorFlag: false
    };
  },
  mounted() {
    if (this.subSets.length !== 0) {
      this.isEmpty = false;
    }
  },
  methods: {
    goDetail(id) {
      router.push("/detail/" + id);
      window.scrollTo(0, 0);
    },
    imgError() {
      this.errorFlag = true;
    }
  }
};
</script>

<style scoped>
.item {
  width: 212px;
  height: 212px;
  margin-left: 10px;
  margin-right: 10px;
  display: inline-block;
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
}
.body_img_hover {
  transition: 0.5s ease;
  opacity: 0;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -90%);
  width: 100%;
  height: 100%;
  display: table;
  align-items: center;
}
.body_img_desc {
  display: table-cell;
  vertical-align: middle;
  color: white;
  text-align: center;
}
.body_img_name {
  font-size: 24px;
}
.body_img_nick {
  font-size: 16px;
  margin-bottom: 15px;
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
  display: flex;
  justify-content: center;
  align-items: baseline;
  transform: translate(10px, -10px);
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

@media screen and (max-width: 600px) {
  .item {
    width: 32vw;
    height: 32vw;
    margin: 0;
  }
  .body_img_hover {
    display: none;
  }
}
</style>
