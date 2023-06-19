<template>
  <div id="cont">
    <CardView title="Sign Up">
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
          :rules="[(val) => (val && val.length > 0) || 'Please type something']"
        />

        <q-select
          filled
          v-model="membership"
          :options="options"
          :option-value="(item) => item.label"
          label="Membership Type"
          emit-value
        />

        <div id="buttons">
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
    </CardView>
  </div>
</template>

<script>
import CardView from "src/components/CardView.vue";
import { signup } from "../services/Api";

export default {
  name: "SignUpView",
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
          this.$q.notify({
            type: "positive",
            message: "Successfully Logged In.",
          });
          return resp;
        })
        .catch((err) => {
          this.$q.notify({
            type: "negative",
            message: err.response.data.message,
          });
          if (Object.values(err.response.data.errors)) {
            this.$q.notify({
              type: "negative",
              message: Object.values(err.response.data.errors),
            });
          }
        });
    },
    onReset() {
      this.emailAddress = "";
      this.firstName = "";
      this.lastName = "";
      this.password = "";
      this.membership = "";
      this.username = "";
    },
  },
  components: { CardView },
};
</script>
<style scoped>
#cont {
  height: 51rem;
  width: 35rem;
  margin: 40px auto;
}
.btn {
  display: flex;
  justify-content: space-evenly;
  margin: 35px auto;
}
h4 {
  font-size: 2rem;
  padding: 0px 65px;
}

#buttons {
  display: flex;
  justify-content: space-around;
  margin: 50px auto;
  width: 200px;
  height: 25px;
}
</style>
