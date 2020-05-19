<template>
  <div>
    <div id="write_desc_box">
      <div id="title">
        <div class="star">
          *
        </div>
        <v-text-field
          label="제목"
          v-model="params.set_name"
          color="rgba(255, 215, 0, 0.7)"
          outlined
          hide-details
        />
      </div>
      <div id="theme">
        <div class="star">
          *
        </div>
        <v-autocomplete
          v-model="params.theme_name"
          :loading="loading"
          :items="themeList"
          :search-input.sync="search"
          cache-items
          flat
          hide-details
          label="테마를 골라주세요"
          solo-inverted
          color="rgba(255, 215, 0, 0.7)"
          multiple
        ></v-autocomplete>
      </div>
      <div id="tag">
        <div class="star">
          *
        </div>
        <vue-tags-input
          v-model="tag"
          :tags="tags"
          :validation="validation"
          @tags-changed="newTags => (tags = newTags)"
          placeholder=""
          :max-tags="5"
        />
      </div>
      <div id="desc">
        <div class="star">
          *
        </div>
        <v-textarea
          label="내용"
          v-model="params.description"
          auto-grow
          color="rgba(255, 215, 0, 0.7)"
          outlined
          hide-details
        />
      </div>
      <div id="ref">
        <v-text-field
          label="참조"
          v-model="params.reference"
          color="rgba(255, 215, 0, 0.7)"
          outlined
          hide-details
        />
      </div>
    </div>
    <div>
      <button @click="onPrev(step - 1)" class="before_btn">
        이전
      </button>
      <button @click="onNext(step + 1)" class="after_btn">
        다음
      </button>
    </div>
  </div>
</template>

<script>
import LegoThemes from "../../../jsonData/LegoThemes.json";
import { mapState, mapActions, mapMutations } from "vuex";

import VueTagsInput from "@johmun/vue-tags-input";

export default {
  components: {
    VueTagsInput
  },
  data() {
    return {
      tag: "",
      tags: [
        {
          text: "태그는 최대 5개입니다.",
          style: "background-color: gold"
        }
      ],
      validation: [
        {
          classes: "min-length",
          rule: tag => tag.text.length < 2
        },
        {
          classes: "no-numbers",
          rule: /^([^0-9]*)$/
        },
        {
          classes: "avoid-item",
          rule: /^(?!Cannot).*$/,
          disableAdd: true
        },
        {
          classes: "no-braces",
          rule: ({ text }) =>
            text.indexOf("{") !== -1 || text.indexOf("}") !== -1
        }
      ],
      themeHeader: LegoThemes["header"],
      themess: LegoThemes["rows"],
      loading: false,
      themeList: [],
      search: null,
      themes: []
    };
  },
  watch: {
    search(val) {
      val && val !== this.params.theme_name && this.querySelections(val);
    },
    tag() {
      const temp = [];
      this.tags.forEach(e => {
        temp.push(e["text"]);
      });
      const ta = temp.map(s => s);
      this.params.tags = ta;
    }
  },
  computed: {
    ...mapState({
      params: state => state.write.descParams,
      step: state => state.write.step,
      currentStep: state => state.write.currentStep
    })
  },
  async mounted() {
    await this.setThemesList();
    document.querySelector("#tag > div.vue-tags-input > div").style.width =
      "642px";
    document.querySelector(
      "#tag > div.vue-tags-input > div > ul"
    ).style.paddingLeft = "0px";
  },
  methods: {
    ...mapActions("write", ["next"]),
    ...mapActions("write", ["prev"]),
    ...mapMutations("write", ["setSteps"]),
    ...mapMutations("write", ["setCurrentStep"]),
    goStep(idx) {
      if (this.currentStep >= idx || this.step >= idx) {
        this.setCurrentStep(idx);
      }
    },
    onStep(idx) {
      this.setStep(idx);
    },
    validateCheck() {
      if (
        this.params.set_name.length > 50 ||
        this.params.set_name.length <= 2
      ) {
        alert(
          "제목이 너무 길거나 짧습니다. 2글자 이상 50글자 미만으로 작성해 주세요"
        );
        return false;
      } else if (
        !this.params.theme_name ||
        !this.params.tags ||
        !this.params.description
      ) {
        alert("필수 항목을 채워주세요");
        return false;
      }
      return true;
    },
    onNext(idx) {
      const check = this.validateCheck();
      if (check === false) {
        return;
      }
      const params = {
        idx: idx,
        step: 2
      };
      this.next(params);
    },
    onPrev(idx) {
      const check = this.validateCheck();
      if (check === false) {
        return;
      }
      const params = {
        idx: idx,
        step: 2
      };
      this.prev(params);
    },
    querySelections(v) {
      this.loading = true;
      setTimeout(() => {
        this.themeList = this.themes.filter(e => {
          return (e || "").toLowerCase().indexOf((v || "").toLowerCase()) > -1;
        });
        this.loading = false;
      }, 500);
    },
    setThemesList() {
      this.themess.forEach(e => {
        if (e[1] === "NULL") {
          this.themes.push(e[2]);
        } else {
          if (this.themess[e[1] - 1][1] === "NULL") {
            this.themes.push(this.themess[e[1] - 1][2] + " > " + e[2]);
          } else {
            if (this.themess[this.themess[e[1] - 1][1] - 1][1] === "NULL") {
              this.themes.push(
                this.themess[this.themess[e[1] - 1][1] - 1][2] +
                  " > " +
                  this.themess[e[1] - 1][2] +
                  " > " +
                  e[2]
              );
            } else {
              if (
                this.themess[
                  this.themess[this.themess[e[1] - 1][1] - 1][1] - 1
                ][1] === "NULL"
              ) {
                this.themes.push(
                  this.themess[
                    this.themess[this.themess[e[1] - 1][1] - 1][1] - 1
                  ][2] +
                    " > " +
                    this.themess[this.themess[e[1] - 1][1] - 1][2] +
                    " > " +
                    this.themess[e[1] - 1][2] +
                    " > " +
                    e[2]
                );
              }
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
#write_desc_box {
  width: 80%;
  margin: auto;
}
#title,
#theme,
#tag,
#desc,
#ref {
  margin-bottom: 20px;
}
.star {
  position: absolute;
  transform: translateX(5px);
  color: red;
}

.before_btn,
.after_btn {
  background-color: gold;
  padding: 10px;
  border-radius: 20px;
  width: 100px;
  margin-top: 20px;
}
.before_btn:hover,
.after_btn:hover {
  background-color: green;
  color: white;
}
.after_btn {
  float: right;
}
.after_btn:disabled {
  background-color: gray;
  color: black;
}
.after_btn:disabled:hover {
  background-color: gray;
  color: black;
}
</style>
