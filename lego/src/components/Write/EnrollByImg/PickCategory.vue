<template>
  <div>
    <h2 class="lego_category_box">카테고리를 선택하세요</h2>
    <div class="category_items_box">
      <div class="row">
        <div
          class="category_items"
          v-for="(category, idx) in categoryInfo"
          :key="`category${idx}`"
          @click="goPickPart(category.id)"
        >
          <img class="item_pic" :src="category.img" alt="photo" />
          <div class="item_name">
            <p>{{ category.name }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  data() {
    return {
      categoryInfo: []
    };
  },
  computed: {
    ...mapState({
      allParts: state => state.write.legoParts.rows,
      allCategory: state => state.write.legoCategory.rows
    })
  },
  mounted() {
    for (let category of this.allCategory) {
      for (let part of this.allParts) {
        if (category[0] === part[5] && part[2] !== "") {
          this.categoryInfo.push({
            name: category[1],
            img: part[2],
            id: category[0]
          });
          break;
        }
      }
    }
  },
  methods: {
    ...mapActions("write", ["filterParts", "changeStep"]),
    goPickPart(id) {
      this.filterParts(id);
      this.changeStep(1);
    }
  }
};
</script>

<style scoped>
.category_items_box {
  display: flex;
  width: 100%;
  margin: auto;
}
.category_items {
  width: 100px;
  height: 100px;
  position: relative;
  border: 1px solid gold;
  margin: 8.8px;
  background: black;
  cursor: pointer;
}
.row {
  display: flex;
}
.item_pic {
  width: 100%;
  height: 100%;
  top: 0;
  opacity: 1;
  transition: all 0.3s ease-in-out;
}
.item_name {
  position: absolute;
  width: inherit;
  height: inherit;
  top: 0;
  right: 0;
  overflow: hidden;
  line-height: 100px;
  opacity: 0;
  color: white;
  transform: translateY(10px);
  transition: all 0.3s ease-in-out;
  text-align: center;
}
.category_items:hover .item_pic {
  opacity: 0.5;
}
.category_items:hover .item_name {
  opacity: 1;
  transform: translateY(0);
}
</style>
