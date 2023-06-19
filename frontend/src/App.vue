<template>
  <div id="main">
    <HeaderComp />
    <router-view />
    <FooterComp />
  </div>
</template>

<script>
import { defineComponent } from "vue";
import HeaderComp from "./components/HeaderComp.vue";
import FooterComp from "./components/FooterComp.vue";
import { RouterView } from "vue-router";

export default defineComponent({
  name: "App",
  components: { HeaderComp, RouterView, FooterComp },
});
</script>
<style>
#main {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
}
</style>
