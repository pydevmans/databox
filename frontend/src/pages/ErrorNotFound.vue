<template>
  <div
    id="contain404"
    class="bg-white text-white text-center q-pa-md flex flex-center"
  >
    <div>
      <div style="font-size: 30vh; color: black">404</div>

      <div class="text-h2" style="opacity: 0.4">Oops. Nothing here...</div>

      <q-btn
        class="q-mt-xl"
        color="black"
        text-color="blue"
        unelevated
        to="/"
        label="Go Home"
        no-caps
      />
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "ErrorNotFound",
});
</script>
<style>
#contain404 {
  height: 90vh;
}
</style>
