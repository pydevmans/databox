<template>
  <div id="cont">
    <CardView title="Log In">
      <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
        <q-input
          filled
          v-model="username"
          label="Your Username *"
          hint="Username"
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Please type something']"
        />
        <q-input
          v-model="password"
          filled
          :type="isPwd ? 'password' : 'text'"
          hint="Enter your Password"
        >
          <template v-slot:append>
            <q-icon
              :name="isPwd ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd = !isPwd"
            />
          </template>
        </q-input>
        <div class="btn">
          <q-btn label="Submit" type="submit" color="primary" />
          <q-btn
            label="Reset"
            type="reset"
            color="primary"
            flat
            class="q-ml-sm"
            @click="username = password = ''"
          />
        </div>
      </q-form>
    </CardView>
  </div>
</template>

<script>
import CardView from "src/components/CardView.vue";
import { mapActions } from "pinia";
import { useAuthStore } from "src/stores/auth";
import { login } from "../services/Api";

export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
      isPwd: true,
    };
  },
  methods: {
    ...mapActions(useAuthStore, ["loggedIn"]),
    onSubmit() {
      login(this.username, this.password)
        .then((resp) => {
          this.$q.cookies.set("token", resp.data.token);
          this.$router.push("/dashboard");
          this.loggedIn(this.username);
          this.$q.notify({ type: "positive", message: resp.data.data });
          return resp;
        })
        .catch((err) => {
          this.$q.notify({
            type: "negative",
            message:
              err.response.data.message ||
              Object.values(err.response.data.errors),
          });
        });
    },
  },
  components: { CardView },
};
</script>
<style scoped>
#cont {
  height: 27rem;
  width: 32rem;
  margin: 230px auto;
}
.btn {
  display: flex;
  justify-content: space-evenly;
  margin: 35px auto;
}
</style>
