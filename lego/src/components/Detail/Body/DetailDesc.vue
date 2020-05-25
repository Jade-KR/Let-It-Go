<template>
  <div>
    {{ description }}
  </div>
</template>

<script>
export default {
  props: {
    description: {
      type: String,
      default: ""
    }
  }
};
</script>

<style scoped></style>
