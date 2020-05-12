<template>
  <div>
    <div class="container" v-for="i in images.length / 3" :key="i">
      <div class="row">
        <div class="item">
          <div class="img_box">
            <img :src="images[i*3 -3]" alt />
          </div>
        </div>
        <div class="item">
          <div class="img_box">
            <img :src="images[i*3 -2]" alt />
          </div>
        </div>
        <div class="item">
          <div class="img_box">
            <img :src="images[i*3 -1]" alt />
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
.container {
  height: 100%;
  width: 100%;
}
.row {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-around;
  border-style: none;
  height: 100%;
  margin-bottom: 25px;
}
.item {
  width: 260px;
  height: 250px;
}
.img_box {
  width: 100%;
  height: 100%;
  border-radius: 180%;
}
.img_box > img {
  width: 100%;
  height: 100%;
  border-radius: 180%;
}
</style>