<template>
  <div>
    <div class="whole_box" v-for="i in images.length / 3" :key="i">
      <div class="row">
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*3 -3]" alt />
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
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*3 -2]" alt />
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
        <div class="item">
          <div class="body_img_box">
            <img class="body_img" :src="images[i*3 -1]" alt />
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
  </div>
</template>
<script>
export default {
  data() {
    return {
      images: [
        "https://www.lego.com/cdn/cs/set/assets/blt13e6e2a178c38704/Spiderman-Sidekick-Tall-1.jpg?fit=crop&width=800&height=600&quality=80",
        "https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1472457974886-0ebcd59440cc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1526505262320-81542978f63b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1542410613-d073472c3135?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1560167016-022b78a0258e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1517242810446-cc8951b2be40?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1538448174498-9956c159edb0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1517232202491-70f954c23ed4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60"
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
  margin-bottom: 30px;
  justify-content: center;
}
.item {
  width: 260px;
  height: 250px;
  margin-left: 15px;
  margin-right: 15px;
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
  transform: translate(-50%, -100%);
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