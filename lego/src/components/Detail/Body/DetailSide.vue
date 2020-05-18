<template>
  <div>
    <div id="detail-side-box">
      <div id="detail-side-desc">
        <div id="detail-side-title">
          <!-- <b>WHATISTHISWHATIST HISWHATISTHI SWHATISTHISWHATISTHIS</b> -->
          <b>깃으로만든레고 여러분도할수있슴다</b>
        </div>

        <hr class="divide-line" />

        <div id="detail-side-designers">
          <div id="detail-side-designer">
            Designer
          </div>
          <div id="detail-side-designer-id">
            <b>네모나게강렬한아기상어</b>
          </div>
        </div>
        <div id="detail-side-bricks">
          <div id="detail-side-brick">
            Bricks
          </div>
          <div id="detail-side-part">
            <b>1425 Parts</b>
          </div>
        </div>
        <div id="detail-side-tags">
          <div id="detail-side-tag">
            Tags
          </div>
          <div id="detail-side-taglist">
            <b>#Lego #JS #GIT #LOGNLGON</b>
          </div>
        </div>
      </div>

      <hr class="divide-line" />

      <div id="detail-side-number">
        <div id="detail-side-scores">
          <div id="detail-side-score">
            Score
          </div>
          <div id="detail-side-score-num">
            5.0
          </div>
        </div>
        <div id="detail-side-likes" @click="isLike()" v-if="likeFlag == false">
          <div id="detail-side-like">
            Like
          </div>
          <div id="detail-side-like-num">
            12
          </div>
        </div>
        <button id="detail-side-onlikes" @click="isLike()" v-else>
          <i class="fas fa-heart" />
        </button>
      </div>

      <hr class="divide-line" />

      <div id="detail-side-similar">
        <div id="detail-side-similar-text">
          You Can Make
        </div>
        <div id="detail-side-similar-percent">
          86%
        </div>
      </div>
    </div>
    <div id="detail-side-ad">
      <div id="detail-side-content">
        레고레일로 분류를 해보세요!
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      likeFlag: false,
      followFlag: false,
      checked: [
        {
          backgroundColor: "red",
          color: "white"
        }
      ],
      unchecked: [
        {
          backgroundColor: "rgba(0,0,0,0)",
          color: "black"
        }
      ]
    };
  },
  methods: {
    isLike() {
      if (this.likeFlag === false) {
        this.likeFlag = true;
      } else {
        this.likeFlag = false;
      }
    },
    isFollow() {
      if (this.followFlag === false) {
        this.followFlag = true;
      } else {
        this.followFlag = false;
      }
    }
  }
};
</script>

<style scoped>
#detail-side-box {
  /* border: 1px solid black; */
  /* background-color: rgba(255, 215, 0, 0.6); */
  border: 3px solid gold;
  padding: 10px;
}
.divide-line {
  border: 1px solid gold;
  margin: 20px 0;
}
#detail-side-desc {
  text-align: center;
  overflow: hidden;
}
#detail-side-title {
  font-size: 24px;
  margin-top: 20px;
  margin-bottom: 10px;
}
#detail-side-designers,
#detail-side-bricks,
#detail-side-tags {
  display: flex;
  text-align: start;
}
#detail-side-designer,
#detail-side-brick,
#detail-side-tag {
  width: 90px;
  padding: 5px 0;
  font-size: 18px;
}
#detail-side-designer-id,
#detail-side-part,
#detail-side-taglist {
  width: 200px;
  padding: 5px 0 5px 10px;
  /* text-align: start; */
}
#detail-side-number {
  display: flex;
}
#detail-side-scores,
#detail-side-likes {
  width: 50%;
  border: 1px solid green;
  margin: 10px;
  text-align: center;
}
#detail-side-score,
#detail-side-like {
  font-size: 20px;
}
#detail-side-score-num,
#detail-side-like-num {
  font-size: 40px;
}
#detail-side-similar {
  text-align: center;
}
#detail-side-similar-text {
  font-size: 28px;
}
#detail-side-similar-percent {
  font-size: 64px;
}

#detail-side-likes {
  cursor: pointer;
  transition: 0.5s;
}
#detail-side-onlikes {
  width: 50%;
  cursor: pointer;
  font-size: 80px;
  color: red;
}
#detail-side-likes:hover {
  background-color: red;
  color: white;
}

#detail-side-ad {
  margin-top: 10px;
  background-color: rgba(255, 215, 0, 0.6);
  height: 200px;
  text-align: center;
  padding: 20px;
}
#detail-side-content {
  font-size: 24px;
  vertical-align: middle;
}
</style>
