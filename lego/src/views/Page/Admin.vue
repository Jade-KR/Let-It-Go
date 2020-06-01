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
      <div>
        <table>
          <tr>
            <th>
              ID
            </th>
            <th>
              NAME
            </th>
            <th>
              BRANCH
            </th>
            <th>
              TEL
            </th>
            <th>
              ADDRESS
            </th>
            <th>
              DELETE
            </th>
          </tr>
          <tr v-for="i in 10" :key="i">
            <th>
              i
            </th>
            <th>
              i
            </th>
            <th>
              i
            </th>
            <th>
              i
            </th>
            <th>
              i
            </th>
            <th>
              <div class="deleteBtn">
                DELETE
              </div>
            </th>
          </tr>
        </table>

        <div class="loadMore">
          더보기
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapMutations } from "vuex";
import router from "../../router";

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
      // if ( this.userFlag == false) {
      //   this.userFlag = true
      //   this.reviewFlag = false
      //   this.storeFlag = false
      // } else {
      //   this.userFlag = false
      // }
      // this.getUserData()
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
        this.storeFlag = false;
      } else {
        this.reviewFlag = false;
      }
      // const params = {
      //   page: 1,
      //   append: true,
      //   page_size: 10,
      //   reset: true,
      // };
      // await this.getUserReview(params);
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
      if (this.storeFlag == false) {
        this.storeFlag = true;
        this.userFlag = false;
        this.reviewFlag = false;
      } else {
        this.storeFlag = false;
      }
      // const params = {
      //   page: 1,
      //   append: true,
      //   page_size: 10,
      //   reset: true,
      // };
      // await this.getStores(params)
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
