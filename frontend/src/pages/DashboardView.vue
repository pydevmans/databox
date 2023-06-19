<template>
  <h4>Welcome, {{ this.username }}!</h4>
  <p>Find here all overview of all databases and profile!</p>
  <div id="cont">
    <CardView title="Database">
      <ul>
        <template v-for="db in this.databases" v-bind:key="db">
          <li>
            <a :href="`/users/${this.username}/databases/${db}`">{{ db }}</a>
          </li>
        </template>
      </ul>
    </CardView>
    <CardView title="Profile">
      <form>
        <q-input
          filled
          v-model="this.firstname"
          label="First Name"
          placeholder="Placeholder"
          disable
        />
        <q-input
          filled
          v-model="lastname"
          label="Last Name"
          placeholder="Placeholder"
          disable
        />
        <q-input
          filled
          v-model="userName"
          label="Username"
          placeholder="Placeholder"
          disable
        />
        <q-input
          filled
          v-model="email"
          label="Email Address"
          placeholder="Placeholder"
          disable
        />
        <q-input
          filled
          v-model="membership"
          label="Membership"
          placeholder="Placeholder"
          disable
        />
      </form>
    </CardView>
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
      databases: [],
      firstname: "",
      lastname: "",
      email: "",
      membership: "",
      userName: "",
    };
  },
  beforeRouteEnter(to, from, next) {
    const promise1 = viewDatabase("user2").then((res) => res);
    const promise2 = viewProfile("user2").then((res) => res);
    let prmsList = [promise1, promise2];
    Promise.allSettled(prmsList).then((results) => {
      next((vm) => {
        vm.setDatabase(results[0].value.data.data);
        vm.setProfile(results[1].value.data.data.userdata);
      });
    });
  },
  computed: {
    ...mapState(useAuthStore, ["username"]),
  },
  methods: {
    setDatabase(data) {
      this.databases = data;
    },
    setProfile(userdata) {
      this.firstname = userdata[1];
      this.lastname = userdata[2];
      this.email = userdata[5];
      this.userName = userdata[3];
      this.membership = userdata[6];
    },
  },
  components: { CardView },
};
</script>
<style scoped>
#cont {
  min-height: 68vh;
  width: 90rem;
  margin: 40px auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}
h4 {
  font-size: 2rem;
  padding: 0px 65px;
}
</style>
