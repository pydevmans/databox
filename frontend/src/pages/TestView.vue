<template>
  <div id="cont">
    <CardView title="Database"> </CardView>
  </div>
</template>

<script>
import { viewDatabase, viewProfile } from "../services/Api";
import { useAuthStore } from "src/stores/auth";
import { mapState } from "pinia";
import CardView from "src/components/CardView.vue";
export default {
  name: "TestDashboardView",
  data() {
    return {
      userName: "",
    };
  },
  beforeRouteEnter(to, from, next) {},
  computed: {},
  methods: {},
  created() {},
  components: { CardView },
};
</script>
<style scoped></style>
