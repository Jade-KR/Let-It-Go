<template>
  <div>
    <v-dialog v-model="userCategory" width="750px">
      <template v-slot:activator="{ on }">
        <div v-on="on"><slot name="userCategory" /></div>
      </template>
      <v-card class="userCategory" color="white">
        <div id="category_box">
          <div id="category_border">
            <div id="category_header">
              당신의 선호 카테고리를 골라주세요
            </div>
            <hr id="divied_line" />
            <div id="category_main">
              <div
                v-for="(category, i) in categories"
                :key="`category-${i}`"
                class="categories category_img_box"
                @click="check(i)"
              >
                <img
                  class="category_img"
                  :src="category[1]"
                  alt="category_image"
                />
                <div class="category_desc" :id="`img_hover-${i}`">
                  <span class="cate_text">{{ category[0] }}</span>
                  <br />
                  <span class="cate_text">{{ category[2] }}</span>
                </div>
              </div>
            </div>
            <hr id="divied_line" />
            <div id="category_submit" @click="submit()">
              선택완료
            </div>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  data() {
    return {
      userCategory: false,
      categories: [
        ["건축물", "/images/category/architecture.jpg", "architecture"],
        ["장난감", "/images/category/toy.jpg", "toy"],
        ["공상과학", "/images/category/SF.jpg", "SF"],
        ["레이싱", "/images/category/racing.jpg", "racing"],
        ["클래식", "/images/category/classic.jpg", "classic"],
        ["창작품", "/images/category/creation.jpg", "creation"],
        ["게임", "/images/category/game.jpg", "game"],
        ["히어로", "/images/category/hero.jpg", "hero"],
        ["공룡", "/images/category/dinosaurs.jpg", "dinosaurs"]
      ],
      checkObj: {
        건축물: 0,
        장난감: 0,
        공상과학: 0,
        레이싱: 0,
        클래식: 0,
        창작품: 0,
        게임: 0,
        히어로: 0,
        공룡: 0
      },
      params: []
    };
  },
  methods: {
    ...mapActions("home", ["setUserCategory"]),
    check(idx) {
      const target = document.getElementById(`img_hover-${idx}`);
      if (target.style.opacity === "1") {
        target.style.opacity = "";
        this.checkObj[this.categories[idx][0]] = 0;
      } else {
        target.style.opacity = "1";
        this.checkObj[this.categories[idx][0]] = 1;
      }
    },
    submit() {
      for (let i in this.checkObj) {
        if (this.checkObj[i]) {
          this.params.push(i);
        }
      }
      if (this.params.length === 0) {
        alert("선호 카테고리를 선택해주세요");
        return;
      }
      const params = {
        categories: ""
      };
      params["categories"] = this.params.join("|");
      this.setUserCategory(params);
      this.userCategory = false;
      this.$emit("cateSubmit", true);
    }
  }
};
</script>

<style scoped>
.category_img_box {
  width: 50%;
  height: 50%;
  position: relative;
  margin-bottom: 10px;
}
.category_img_box > img {
  width: 210px;
  height: 210px;
  border: 1px solid gold;
  padding: 5px;
  transform: translateY(5.5px);
  cursor: pointer;
}
.category_desc {
  width: 210px;
  height: 210px;
  background-color: rgba(0, 0, 0, 0.6);
  position: absolute;
  transform: translate(60px, -210px);
  opacity: 0;
  transition: 0.5s ease;
  color: white;
  padding-top: 70px;
  cursor: pointer;
}
.category_desc:hover {
  opacity: 1;
}
.cate_text {
  font-size: 22px;
  font-weight: 600;
}

#category_box {
  padding: 10px;
}
#category_border {
  border: 3px solid gold;
  border-radius: 10px;
  padding: 10px;
}
#category_header {
  text-align: center;
  margin-top: 10px;
  margin-bottom: 20px;
  font-size: 30px;
  font-weight: 600;
}
#divied_line {
  width: 90%;
  border: 1px dashed gold;
  margin: auto;
  margin-bottom: 10px;
}
#category_main {
  padding: 10px;
  text-align: center;
}
.categories {
  width: 50%;
  display: inline-block;
}
#category_submit {
  width: 60%;
  margin: auto;
  line-height: 50px;
  font-size: 24px;
  font-weight: 600;
  border: 1px solid gold;
  text-align: center;
  cursor: pointer;
  border-radius: 15px;
}
#category_submit:hover {
  background-color: gold;
  color: white;
}
</style>
