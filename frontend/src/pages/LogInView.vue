<template>
  <div id="login" class="shadow-10">
    <h4>Log In</h4>
    <div id="loginform">
      <div class="q-pa-md" style="max-width: 400px">
        <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
          <q-input
            filled
            v-model="username"
            label="Your Username *"
            hint="Username"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
            ]"
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
          <div>
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
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "stores/auth";
import { login } from "../services/Api";
import { mapActions } from "pinia";
export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
      isPwd: true,
    };
  },
  computer: {},
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
};
</script>
<style scoped>
#login {
  display: flex;
  flex-flow: column;
  margin: 100px auto;
  height: 35rem;
  width: 35rem;
  border: 1px solid black;
  border-radius: 2rem;
}

#loginform {
  color: var(--vt-c-black);
  flex-grow: 1;
  margin: 0 auto;
}

h4 {
  font-size: 2rem;
  padding: 25px 25px;
}

form {
  display: grid;
  height: 100%;
  justify-content: center;
  align-content: center;
}

label {
  display: block;
  font-size: 1.5rem;
  color: var(--theme-color-dark);
}

input {
  display: block;
  width: 200px;
  height: 2rem;
  border-radius: 0.25rem;
}

#btn {
  display: flex;
  justify-content: space-around;
  margin: 15px auto;
  width: 200px;
  height: 25px;
}

button {
  background-color: var(--theme-color);
  border-radius: 10px;
  box-shadow: inset 2px 2px 3px rgba(255, 255, 255, 0.6),
    inset -2px -2px 3px rgba(0, 0, 0, 0.6);
  height: 30px;
  width: 75px;
}
</style>
