<script>
import { viewDatabase } from "../services/Api";
import { defineComponent } from "vue";
export default defineComponent({
  name: "HomeView",
  data() {
    return {
      data: "",
    };
  },
  methods: {
    fetchDash() {
      viewDatabase("user2").then((resp) => {
        this.data = resp.data;
      });
    },
  },
  created() {
    this.fetchDash();
  },
});
</script>

<template>
  {{ this.data }}
</template>

<style scoped></style>
