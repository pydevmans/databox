<script>
import { home } from "../services/Api";
import { defineComponent } from "vue";
export default defineComponent({
  name: "HomeView",
  data() {
    return {
      data: "",
    };
  },
  methods: {
    fetchHome() {
      home().then((resp) => (this.data = resp.data));
    },
  },
  created() {
    this.fetchHome();
  },
});
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
      <p>
        For logged in user related help:
        <RouterLink to="/helpcenter">Help Center</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
#homeview {
  display: block;
  min-height: 92vh;
  width: 800px;
  margin: 10px auto;
}

h2 {
  font-size: larger;
  text-align: center;
  font-size: 26px;
}

h4 {
  font-size: large;
  padding: 10px 0px;
}

li {
  margin-left: 20px;
  list-style: square;
}

#help {
  margin-top: 50px;
}
</style>
