<template>
  <div id="card" class="shadow-10">
    <h4>{{ title }}</h4>
    <div id="carditem">
      <div class="cardcontent">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CardView",
  props: ["title"],
};
</script>
<style scoped>
#card {
  border: 1px solid black;
  border-radius: 2rem;
  height: 100%;
  padding: 25px 25px;
}
h4 {
  font-size: 2rem;
  padding: 0px 65px;
}

#carditem {
  color: var(--vt-c-black);
  margin: 0px auto;
}

.cardcontent {
  width: fit-content;
  margin: 0px auto;
}
</style>
