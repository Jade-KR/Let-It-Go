<template>
  <div>
    <div id="tabs">
      <div id="tab1" class="tab" @click="showModels()">
        Models
      </div>
      <div id="tab2" class="tab" @click="showReviews()">
        Reviews
      </div>
      <div id="tab3" class="tab" @click="showUsers()">
        Users
      </div>
      <div class="tab" @click="goHome()">
        돌아가기
      </div>
    </div>
    <div>
      <div v-if="modelFlag === true">
        <table>
          <tr>
            <th>
              ID
            </th>
            <th>
              NAME
            </th>
            <th>
              WRITER
            </th>
            <th>
              LIKE COUNT
            </th>
            <th>
              REVIEW COUNT
            </th>
            <th>
              DELETE
            </th>
          </tr>
          <tr v-for="(v, i) in models" :key="`models-${i}`">
            <th>
              {{ v.id }}
            </th>
            <th>
              {{ v.name }}
            </th>
            <th>
              {{ v.nickname }}
            </th>
            <th>
              {{ v.like_count }}
            </th>
            <th>
              {{ v.review_count }}
            </th>
            <th>
              <div class="deleteBtn" @click="delModel(v.id)">
                DELETE
              </div>
            </th>
          </tr>
        </table>

        <div class="loadMore" @click="moreModel()">
          더보기
        </div>
      </div>

      <div v-if="reviewFlag === true">
        <table>
          <tr>
            <th>
              ID
            </th>
            <th>
              USER ID
            </th>
            <th>
              NICKNAME
            </th>
            <th>
              SCORE
            </th>
            <th>
              CONTENT
            </th>
            <th>
              DELETE
            </th>
          </tr>
          <tr v-for="(review, i) in reviews" :key="`review-${i}`">
            <th>
              {{ review.id }}
            </th>
            <th>
              {{ review.user_id }}
            </th>
            <th>
              {{ review.nickname }}
            </th>
            <th>
              {{ review.score }}
            </th>
            <th>
              {{ review.content }}
            </th>
            <th>
              <div class="deleteBtn" @click="delReview(review.id)">
                DELETE
              </div>
            </th>
          </tr>
        </table>

        <div class="loadMore" @click="moreReview()">
          더보기
        </div>
      </div>

      <div v-if="userFlag === true">
        <table>
          <tr>
            <th>
              PK
            </th>
            <th>
              ID
            </th>
            <th>
              NICKNAME
            </th>
            <th>
              E-MAIL
            </th>
            <th>
              IS STAFF
            </th>
            <th>
              AGE
            </th>
            <th>
              GENDER
            </th>
            <th>
              DELETE
            </th>
          </tr>
          <tr v-for="(v, i) in users" :key="`user-${i}`">
            <th>
              {{ v.id }}
            </th>
            <th>
              {{ v.username }}
            </th>
            <th>
              {{ v.nickname }}
            </th>
            <th>
              {{ v.email }}
            </th>
            <th>
              {{ v.is_staff }}
              <div
                style="display: inline;"
                class="chageBtn"
                @click="changeStaff(v.id)"
                v-if="v.username !== myName"
              >
                권한변경
              </div>
            </th>
            <th>
              {{ v.age }}
            </th>
            <th v-if="v.gender === 0">
              남
            </th>
            <th v-else>
              여
            </th>
            <th>
              <div
                class="deleteBtn"
                @click="delUser(v.id)"
                v-if="v.username !== myName"
              >
                DELETE
              </div>
            </th>
          </tr>
        </table>

        <div class="loadMore" @click="moreUser()">
          더보기
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations } from "vuex";
import router from "../../router";

export default {
  data() {
    return {
      modelFlag: false,
      reviewFlag: false,
      userFlag: false,
      myName: localStorage.getItem("username")
    };
  },
  computed: {
    ...mapState({
      modelPage: s => s.admin.modelPage,
      models: s => s.admin.modelList,
      userPage: s => s.admin.userPage,
      users: s => s.admin.userList,
      reviewPage: s => s.admin.reviewPage,
      reviews: s => s.admin.reviewList
    })
  },
  async mounted() {
    const isStaff = localStorage.getItem("isStaff");
    if (isStaff !== "true") {
      router.push("/");
      return;
    }
    await this.setAuthFlag(true);
  },
  destroyed() {
    this.setAuthFlag(false);
  },
  methods: {
    ...mapActions("admin", [
      "getModels",
      "deleteModel",
      "getUsers",
      "deleteUser",
      "isStaff",
      "getReviews",
      "deleteReview"
    ]),
    ...mapMutations("auth", ["setAuthFlag"]),
    goHome() {
      router.push("/");
    },
    async showUsers() {
      var target = document.getElementById("tab3").style;
      var else1 = document.getElementById("tab1").style;
      var else2 = document.getElementById("tab2").style;
      if (target.color == "") {
        target.color = "white";
        target.backgroundColor = "gold";
        else1.color = "";
        else1.backgroundColor = "";
        else2.color = "";
        else2.backgroundColor = "";
      } else {
        target.color = "";
        target.backgroundColor = "";
      }
      if (this.userFlag == false) {
        this.userFlag = true;
        this.reviewFlag = false;
        this.modelFlag = false;
      } else {
        this.userFlag = false;
      }
      const params = {
        page: 1,
        append: false
      };
      await this.getUsers(params);
    },
    async delUser(user_id) {
      await this.deleteUser(user_id);
    },
    async moreUser() {
      const params = {
        append: true,
        page: this.userPage
      };
      await this.getUsers(params);
    },
    async changeStaff(value) {
      this.isStaff(value);
    },

    async showReviews() {
      var target = document.getElementById("tab2").style;
      var else1 = document.getElementById("tab1").style;
      var else2 = document.getElementById("tab3").style;
      if (target.color == "") {
        target.color = "white";
        target.backgroundColor = "gold";
        else1.color = "";
        else1.backgroundColor = "";
        else2.color = "";
        else2.backgroundColor = "";
      } else {
        target.color = "";
        target.backgroundColor = "";
      }
      if (this.reviewFlag == false) {
        this.reviewFlag = true;
        this.userFlag = false;
        this.modelFlag = false;
      } else {
        this.reviewFlag = false;
      }
      const params = {
        page: 1,
        append: false
      };
      await this.getReviews(params);
    },
    async delReview(review_id) {
      await this.deleteReview(review_id);
    },
    async moreReview() {
      const params = {
        append: true,
        page: this.reviewPage
      };
      await this.getReviews(params);
    },

    async showModels() {
      var target = document.getElementById("tab1").style;
      var else1 = document.getElementById("tab2").style;
      var else2 = document.getElementById("tab3").style;
      if (target.color == "") {
        target.color = "white";
        target.backgroundColor = "gold";
        else1.color = "";
        else1.backgroundColor = "";
        else2.color = "";
        else2.backgroundColor = "";
      } else {
        target.color = "";
        target.backgroundColor = "";
      }
      if (this.modelFlag == false) {
        this.modelFlag = true;
        this.userFlag = false;
        this.reviewFlag = false;
      } else {
        this.modelFlag = false;
        return;
      }
      const params = {
        page: 1,
        append: false
      };
      await this.getModels(params);
    },
    async delModel(set_id) {
      await this.deleteModel(set_id);
    },
    async moreModel() {
      const params = {
        append: true,
        page: this.modelPage
      };
      await this.getModels(params);
    }
  }
};
</script>

<style scoped>
.tab {
  border: 1px solid gold;
  display: inline-block;
  width: 24vw;
  padding: auto;
  font-size: 50px;
  text-align: center;
  cursor: pointer;
}
.tab:hover {
  background-color: gold;
  color: white;
}
.loadMore {
  font-size: 40px;
  text-align: center;
  cursor: pointer;
}
table {
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
  border: 1px solid #ddd;
}
th {
  text-align: left;
  padding: 16px;
}
tr:nth-child(even) {
  background-color: #ddd;
}
.deleteBtn {
  border: 1px solid gold;
  padding: 1px;
  text-align: center;
  background-color: red;
  color: white;
  cursor: pointer;
}
.chageBtn {
  border: 1px solid gold;
  padding: 1px;
  text-align: center;
  background-color: green;
  color: white;
  cursor: pointer;
}
</style>
