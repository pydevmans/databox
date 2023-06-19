<template>
  <div id="header">
    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/features">Features</RouterLink>
      <RouterLink v-if="authStatus" to="/dashboard">Dashboard</RouterLink>
      <!-- <RouterLink to="/dashboard/<database:str>">Database</RouterLink> -->
      <!-- <RouterLink to="/dashboard/<database:str>/query?page=2">Database</RouterLink> -->
      <RouterLink v-if="!authStatus" to="/login">Log In</RouterLink>
      <RouterLink v-if="!authStatus" to="/signup">Sign Up</RouterLink>
      <RouterLink v-if="authStatus" to="/logout">Logout</RouterLink>
    </nav>
  </div>
</template>

<style scoped>
nav {
  text-align: right;
}
nav > a {
  font-size: larger;
  padding: 0 5px;
}
</style>
<script>
import { useAuthStore } from "stores/auth";
import { mapState } from "pinia";

export default {
  name: "HeaderComp",
  computed: {
    ...mapState(useAuthStore, ["authStatus"]),
  },
};
</script>
