<template>
  <div id="features">
    <div class="product product1 shadow-10">
      <h4>Free Membership</h4>
      <ul>
        <li>Database Limit: {{ this.data.data.freefeats.database_limit }}</li>
      </ul>
      <ul>
        <li>Record Limit: {{ this.data.data.freefeats.record_limit }}</li>
      </ul>
      <ul>
        <h5>Features</h5>
        <li v-for="item in this.data.data.freefeats.feat" :key="item">
          {{ item }}
        </li>
      </ul>
    </div>
    <div class="product product2 shadow-10">
      <h4>Basic Membership</h4>
      <ul>
        <li>Database Limit: {{ this.data.data.basicfeats.database_limit }}</li>
      </ul>
      <ul>
        <li>Record Limit: {{ this.data.data.basicfeats.record_limit }}</li>
      </ul>
      <ul>
        <h5>Features</h5>
        <li v-for="item in this.data.data.basicfeats.feat" :key="item">
          {{ item }}
        </li>
      </ul>
    </div>
    <div class="product product3 shadow-10">
      <h4>Premium Membership</h4>
      <ul>
        <li>
          Database Limit: {{ this.data.data.premiumfeats.database_limit }}
        </li>
      </ul>
      <ul>
        <li>Record Limit: {{ this.data.data.premiumfeats.record_limit }}</li>
      </ul>
      <ul>
        <h5>Features</h5>
        <li v-for="item in this.data.data.premiumfeats.feat" :key="item">
          {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
#features {
  width: 70%;
  margin: 25px auto;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
}
h4 {
  text-align: center;
}

.product ul {
  list-style-type: none;
}
.product1 li::before {
  content: "✅ ";
}

.product2 li::before {
  content: "🏍️ ";
}

.product3 li::before {
  content: "🚀 ";
}
li {
  font-size: large;
}

.product {
  padding: 25px 25px;
  border: 1px solid grey;
  height: 700px;
  border-radius: 5px;
  margin: 25px 15px;
  min-width: 275px;
}
</style>

<script>
import { features } from "../services/Api";
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
