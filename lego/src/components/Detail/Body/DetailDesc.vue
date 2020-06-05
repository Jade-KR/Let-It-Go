<template>
  <div>
    <div v-if="sentences !== ''">
      <div v-for="(sentence, i) in sentences" :key="i">
        {{ sentence }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    description: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      sentences: ""
    };
  },
  mounted() {
    if (this.description !== null) {
      this.sentences = this.description.split("\n");
    }
  }
};
</script>

<style scoped></style>
