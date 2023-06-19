<template>
  <div id="logout" class="shadow-10">
    <h4>Please wait.</h4>
  </div>
</template>

<script>
import { mapActions } from "pinia";
import { useAuthStore } from "stores/auth";

export default {
  name: "LogOutView",
  mounted() {
    try {
      this.loggedOut();
      this.$q.cookies.remove("token");
      this.$q.notify({
        type: "positive",
        message: "Successsfully Logged Out.",
      });
      this.$router.push("/");
    } catch (e) {
      this.$q.notify({
        type: "negetive",
        message: "Something went wrong! Please try again.",
      });
    }
  },
  methods: {
    ...mapActions(useAuthStore, ["loggedOut"]),
  },
};
</script>
<style scoped>
#logout {
  display: flex;
  flex-flow: column;
  margin: 100px auto;
  height: 35rem;
  width: 35rem;
  border: 1px solid black;
  border-radius: 2rem;
}

h4 {
  font-size: 2rem;
  padding: 25px 25px;
}
</style>
