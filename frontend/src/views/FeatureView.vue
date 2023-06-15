<template>
  <div id="features">
    <div class="product product1">
      <h3>Free Features</h3>
      <ul>
        <li>Database Limit: {{ this.data.freefeats.database_limit }}
        </li>
      </ul>
      <ul>
        <li>Record Limit: {{ this.data.freefeats.record_limit }}
        </li>
      </ul>
      <ul>
        <h4>Features</h4>
        <li v-for="item in data.freefeats.feat" :key="item">
          {{ item }}
        </li>
      </ul>
    </div>
    <div class="product product2">
      <h3>Basic Features</h3>
      <ul>
        <li>Database Limit: {{ this.data.basicfeats.database_limit }}
        </li>
      </ul>
      <ul>
        <li>Record Limit: {{ this.data.basicfeats.record_limit }}
        </li>
      </ul>
      <ul>
        <h4>Features</h4>
        <li v-for="item in data.basicfeats.feat" :key="item">
          {{ item }}
        </li>
      </ul>
    </div>
    <div class="product product3">
      <h3>Premium Features</h3>
      <ul>
        <li>Database Limit: {{ this.data.premiumfeats.database_limit }}
        </li>
      </ul>
      <ul>
        <li>Record Limit: {{ this.data.premiumfeats.record_limit }}
        </li>
      </ul>
      <ul>
        <h4>Features</h4>
        <li v-for="item in data.premiumfeats.feat" :key="item">
          {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
#features {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;

}

.product {
  padding: 25px 25px;
  border: 1px solid grey;
  height: 700px;
  border-radius: 5px;
  margin: 25px 15px
}

h3 {
  text-align: center;
  font-size: 26px;
  background: -webkit-linear-gradient(var(--theme-color), var(--theme-color-dark));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

h4 {
  color: var(--theme-color-dark);
  position: static;
  left: 5px;
  margin: 25px 0;
  font-size: 18px
}
</style>

<script>
import { features } from "../middleware/axios"
import { defineComponent } from "vue";

export default defineComponent({
  "name": "HomeView",
  data() {
    return {
      data: features,
    }
  }
})
</script>