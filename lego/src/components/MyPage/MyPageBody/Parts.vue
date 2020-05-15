<template>
  <div>
    <div class="whole_box" v-for="i in images.length / 8" :key="i">
      <div class="row">
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*8 -8]" alt />
            <div class="part_info">
              <p class="part_id">xfwef1231</p>
              <p class="part_quantity">30 개</p>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*8 - 7]" alt />
            <div class="part_info">
              <p class="part_id">xfwef1231</p>
              <p class="part_quantity">30 개</p>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*8 - 6]" alt />
            <div class="part_info">
              <p class="part_id">xfwef1231</p>
              <p class="part_quantity">30 개</p>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*8 - 5]" alt />
            <div class="part_info">
              <p class="part_id">xfwef1231</p>
              <p class="part_quantity">30 개</p>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*8 - 4]" alt />
            <div class="part_info">
              <p class="part_id">xfwef1231</p>
              <p class="part_quantity">30 개</p>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*8 - 3]" alt />
            <div class="part_info">
              <p class="part_id">xfwef1231</p>
              <p class="part_quantity">30 개</p>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*8 - 2]" alt />
            <div class="part_info">
              <p class="part_id">xfwef1231</p>
              <p class="part_quantity">30 개</p>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*8 - 1]" alt />
            <div class="part_info">
              <p class="part_id">xfwef1231</p>
              <p class="part_quantity">30 개</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      images: [
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/4568951.jpg/85x85p.jpg?1579392688.0645452",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/243626.jpg/85x85p.jpg?1579392269.3131735",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6099909.jpg/85x85p.jpg?1579392608.816664",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6173203.jpg/85x85p.jpg?1579392424.9449399",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6157554.jpg/85x85p.jpg?1579392149.7653546",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6066952.jpg/85x85p.jpg?1579392424.5969403",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/4124111.jpg/85x85p.jpg?1579392691.67654",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6194727.jpg/85x85p.jpg?1579419991.6757934",
        "https://cdn.rebrickable.com/media/thumbs/parts/ldraw/0/422.png/85x85p.png?1579393006.0200706",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/4517925.jpg/85x85p.jpg?1579392221.9452453",
        "https://cdn.rebrickable.com/media/thumbs/parts/ldraw/15/4081a.png/85x85p.png?1579393015.8680558",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/4568951.jpg/85x85p.jpg?1579392688.0645452",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/243626.jpg/85x85p.jpg?1579392269.3131735",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6099909.jpg/85x85p.jpg?1579392608.816664",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6173203.jpg/85x85p.jpg?1579392424.9449399",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6157554.jpg/85x85p.jpg?1579392149.7653546",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6066952.jpg/85x85p.jpg?1579392424.5969403",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/4124111.jpg/85x85p.jpg?1579392691.67654",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6194727.jpg/85x85p.jpg?1579419991.6757934",
        "https://cdn.rebrickable.com/media/thumbs/parts/ldraw/0/422.png/85x85p.png?1579393006.0200706",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/4517925.jpg/85x85p.jpg?1579392221.9452453",
        "https://cdn.rebrickable.com/media/thumbs/parts/ldraw/15/4081a.png/85x85p.png?1579393015.8680558",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/6066952.jpg/85x85p.jpg?1579392424.5969403",
        "https://cdn.rebrickable.com/media/thumbs/parts/elements/4124111.jpg/85x85p.jpg?1579392691.67654"
      ]
    };
  }
};
</script>

<style scoped>
.whole_box {
  height: 100%;
  width: 100%;
}
.row {
  display: flex;
  flex-flow: row nowrap;
  border-style: none;
  height: fit-content;
  margin-bottom: 5px;
  justify-content: center;
}
.item {
  width: 110px;
  height: 140px;
  margin-left: 2px;
  margin-right: 2px;
  border: rgb(205, 205, 228) 3px solid;
}
.item:hover {
  border: rgb(166, 166, 184) 3px solid;
}
.body_img_box {
  width: 100%;
  height: 70%;
  background: black;
  position: relative;
  margin: 0;
  padding: 0;
}
.body_img_box > img {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  /* border-radius: 180%; */
}
.part_info {
  width: 100%;
  height: 44%;
  position: relative;
  background: rgb(248, 248, 248);
  margin: 0;
  padding: 0;
  bottom: 7px;
}
.part_id {
  margin: 0;
  text-align: center;
  font-size: 14px;
}
.part_quantity {
  margin: 0;
  text-align: center;
  font-size: 15px;
}
</style>