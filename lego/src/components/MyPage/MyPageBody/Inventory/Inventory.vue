<template>
  <div>
    <div
      id="model_body"
      v-infinite-scroll="loadMore"
      infinite-scroll-disabled="loading"
      infinite-scroll-distance="10"
    >
      <div v-if="this.userModels.length !== 0">
        <div class="main">
          <div class="whole_box">
            <div
              class="item"
              v-for="(item, idx) in userModels"
              :key="`item${idx}`"
              @click="goDetail(item)"
            >
              <div class="body_img_box">
                <img class="body_img" :src="item.image" alt />
                <div class="body_img_hover">
                  <div class="body_img_desc">
                    <div class="body_img_name">
                      <b>{{ item.name }}</b>
                    </div>
                    <div class="body_img_nick">
                      By. {{ item.user_nickname }}
                    </div>
                    <div class="body_img_info">
                      <i
                        class="fas fa-heart"
                        :style="
                          item.is_like === 1 ? likeStyle[0] : likeStyle[1]
                        "
                      ></i>
                      <span>{{ item.like_count }}</span>
                      <i
                        class="fas fa-comment"
                        :style="
                          item.is_review === 1 ? reviewStyle[0] : reviewStyle[1]
                        "
                      ></i>
                      <span>{{ item.review_count }}</span>
                    </div>
                    <div class="body_img_save">
                      <b style="font-size: 26px; color: gold;">{{
                        item.quantity
                      }}</b
                      >개 보관중
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <NoContentsInventory></NoContentsInventory>
      </div>
    </div>
  </div>
</template>
<script>
import { mapActions, mapState } from "vuex";
import NoContentsInventory from "./NoContentsInventory";
export default {
  components: {
    NoContentsInventory
  },
  data() {
    return {
      loading: true,
      likeStyle: [
        {
          color: "red"
        },
        {
          color: "white"
        }
      ],
      reviewStyle: [
        {
          color: "gold"
        },
        {
          color: "white"
        }
      ]
    };
  },
  async mounted() {
    const params = {
      page: 1,
      append: false
    };
    await this.userModelInven(params);
    if (this.stopScroll === true) {
      return;
    }
    this.loading = false;
  },
  computed: {
    ...mapState({
      userModels: state => state.mypage.invenModelList,
      page: state => state.mypage.invenModelPage,
      stopScroll: state => state.mypage.stopScroll
    })
  },
  methods: {
    ...mapActions("mypage", ["userModelInven"]),
    async loadMore() {
      this.loading = true;
      const params = {
        page: this.page,
        append: true
      };
      await this.userModelInven(params);
      if (this.stopScroll === true) {
        return;
      }
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    },
    goDetail(item) {
      this.$router.push({
        path: `/detail/${item.legoset_id}`
      });
    }
  }
};
</script>

<style scoped>
.main {
  display: flex;
  justify-content: center;
}
.whole_box {
  height: 100%;
  width: 95%;
  display: flex;
  flex-flow: row wrap;
  margin: auto;
}
.item {
  width: 260px;
  height: 250px;
  margin: 14px;
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
  /* position: absolute; */
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
.body_img_save {
  font-size: 20px;
}
@media screen and (max-width: 600px) {
  .main {
    justify-content: start;
    width: 100%;
    height: 100%;
  }
  .whole_box {
    width: 100%;
    height: 100%;
  }
  .item {
    width: 33.3vw;
    height: 33.3vw;
    margin: 0px;
    display: inline-block;
  }
  .body_img_box > img {
    width: 33.3vw;
    height: 33.3vw;
  }
  .body_img_hover {
    display: none;
  }
}
</style>
