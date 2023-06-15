<script>
import { get_home } from "../middleware/axios"
import { defineComponent } from "vue";

export default defineComponent({
  "name": "HomeView",
  data() {
    return {
      data: get_home,
    }
  },
})
</script>

<template>
  <div id="homeview">
    <h2>{{ data.title }}</h2>
    <h4>Application Features</h4>
    <ul>
      <li v-for="item in data.applicationfeatures" :key="item">
        {{ item }}
      </li>
    </ul>
    <h4>Key Highlights</h4>
    <ul>
      <li v-for="item in data.keyhighlights" :key="item">
        {{ item }}
      </li>
    </ul>
    <h4>Tech Stacks</h4>
    <ul>
      <li v-for="item in data.techstacks" :key="item">
        {{ item }}
      </li>
    </ul>
    <div id="help">
      <p>For general help: <RouterLink to="/help">Help</RouterLink>
      </p>
      <p>For logged in user related help: <RouterLink to="/helpcenter">Help Center</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
#homeview {
  display: block;
  height: 860px;
  margin: 10px auto;
}

h2 {
  font-size: larger;
  text-align: center;
  font-size: 26px;
  background: -webkit-linear-gradient(var(--theme-color), var(--theme-color-dark));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

h4 {
  color: var(--theme-color-dark);
  font-size: large;
  padding: 10px 0px;
}

li {
  color: var(--vt-c-black-soft);
  margin-left: 20px;
  list-style: square;
}

#help {
  position: absolute;
  bottom: 0px;
  padding: 0 0 50px 0;
}
</style>
