<template>
  <div id="features"></div>
</template>

<style scoped></style>

<script>
import { viewRecords } from "../services/Api";
import { defineComponent } from "vue";

export default defineComponent({
  name: "FeatureView",
  data() {
    return {
      data: "",
    };
  },
  methods: {
    fetchData() {
      features().then((resp) => (this.data = resp.data));
    },
  },
  created() {
    this.fetchData();
  },
});
</script>
