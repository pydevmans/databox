<template>
  <div id="login">
    <h3>Log In</h3>
    <div id="loginform">
      <form method="post" action="." @submit.prevent="this.formSubmitting">
        <label>Username: </label>
        <input type="text" v-model="username">
        <label>Password: </label>
        <input type="password" v-model="password">
        <div id="btn">
          <button type="reset">Reset</button>
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
#login {
  display: flex;
  flex-flow: column;
  margin: 100px auto;
  height: 35rem;
  width: 35rem;
  border: 1px solid var(--theme-color-dark);
  border-radius: 2rem;
}

#loginform {
  color: var(--vt-c-black);
  flex-grow: 1;
}

h3 {
  font-size: 2rem;
  background: -webkit-linear-gradient(var(--theme-color), var(--theme-color-dark));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
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
  box-shadow: inset 2px 2px 3px rgba(255, 255, 255, 0.6), inset -2px -2px 3px rgba(0, 0, 0, 0.6);
  height: 30px;
  width: 75px;
}
</style>

<script>
import { defineComponent } from 'vue';
export default defineComponent({
  name: "LogInView",
  data() {
    return {
      "username": "",
      "password": "",
    }
  },
  methods: {
    formSubmitting: function () {
      let formData = new FormData();
      formData.append("username", this.username);
      formData.append("password", this.password);
      let URL = "http://127.0.0.1:5000"

      fetch(URL + "/login", { method: "post", body: formData })
        .then(resp => {
          console.log("resp", resp);
          if (resp.ok == "Login Successful!") {
            console.log("Success!");
          }
        })

    }
  }
})
</script>