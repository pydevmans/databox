<template>
  <div id="login" class="shadow-10">
    <h4>Sign Up</h4>
    <div id="loginform">
      <div class="q-pa-md" style="max-width: 400px">
        <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
          <q-input
            filled
            type="text"
            v-model="firstName"
            label="Your First Name"
            lazy-rules
            :rules="[
              (val) =>
                (val !== null && val !== '') || 'Please type your Password',
              // (val) => val > 0 || 'Please type a real age',
            ]"
          />
          <q-input
            filled
            type="text"
            v-model="lastName"
            label="Your Last Name"
            lazy-rules
            :rules="[
              (val) =>
                (val !== null && val !== '') || 'Please type your Password',
              // (val) => val > 0 || 'Please type a real age',
            ]"
          />
          <q-input
            filled
            type="email"
            v-model="emailAddress"
            label="Your Email address"
            lazy-rules
            :rules="[
              (val) =>
                (val !== null && val !== '') || 'Please type your Password',
            ]"
          />
          <q-input
            v-model="password"
            filled
            :type="isPwd ? 'password' : 'text'"
            hint="Enter your password"
          >
            <template v-slot:append>
              <q-icon
                :name="isPwd ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="isPwd = !isPwd"
              />
            </template>
          </q-input>

          <q-input
            filled
            v-model="username"
            label="Your Username *"
            hint="Enter Username"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
            ]"
          />

          <q-select
            filled
            v-model="membership"
            :options="options"
            :option-value="(item) => item.label"
            label="Membership Type"
            emit-value
          />

          <div>
            <q-btn label="Submit" type="submit" color="primary" />
            <q-btn
              label="Reset"
              type="reset"
              color="primary"
              flat
              class="q-ml-sm"
            />
          </div>
        </q-form>
      </div>
    </div>
  </div>
</template>

<script>
import { useQuasar } from "quasar";
import { signup } from "../services/Api";

export default {
  name: "LoginView",
  setup() {
    function getNotify() {
      const $q = useQuasar();
      $q.notify({
        color: "green-4",
        textColor: "white",
        icon: "cloud_done",
        message: "Submitted",
      });
    }
    return {
      getNotify,
    };
  },
  data() {
    return {
      username: "",
      password: "",
      emailAddress: "",
      firstName: "",
      lastName: "",
      membership: "",
      isPwd: true,
      options: [
        { label: "Free", value: 0 },
        { label: "Basic", value: 1 },
        { label: "Premium", value: 2 },
      ],
    };
  },
  methods: {
    onSubmit() {
      signup(
        this.username,
        this.password,
        this.emailAddress,
        this.firstName,
        this.lastName,
        this.membership
      )
        .then((resp) => {
          console.log("[AXIOS RESP]", resp);
          return resp;
        })
        .catch((err) => console.log("ERROR", err));
      // this.getNotify();
    },
    onReset() {
      this.emailAddress = "";
      this.firstName = "";
      this.lastName = "";
      this.password = "";
      this.membership = "";
      this.username = "";
    },
    // onToggle() {
    //   this.isPwd = !this.isPwd;
    // },
  },
};
</script>
<style scoped>
#login {
  display: flex;
  flex-flow: column;
  margin: 100px auto;
  height: 55rem;
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
