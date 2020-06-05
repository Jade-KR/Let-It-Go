<template>
  <div class="text-center">
    <PickCategory v-if="currentStep === 0"></PickCategory>
    <PickPart v-if="currentStep === 1"></PickPart>
    <AddPart v-if="currentStep === 2" @close="close()"></AddPart>
  </div>
</template>

<script>
import { mapState } from "vuex";
import PickCategory from "./SearchByImg/PickCategory";
import PickPart from "./SearchByImg/PickPart";
import AddPart from "./SearchByImg/AddPart";
export default {
  components: {
    PickCategory,
    PickPart,
    AddPart
  },
  data() {
    return {
      page: 1
    };
  },
  computed: {
    ...mapState({
      allParts: state => state.Parts.legoParts.rows,
      currentStep: state => state.Parts.currentStep
    })
  },
  methods: {
    close() {
      this.$emit("close");
    }
  }
};
</script>

<style scoped>
</style>