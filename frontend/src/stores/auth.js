import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    authStatus: false,
    username: ""
  }),
  getters: {
    isAuth: (state) => state.authStatus,
    getUsername: (state) => state.username
  },
  actions: {
    loggedIn(username) {
      this.authStatus = true;
      this.username = username;
      return this.authStatus
    },
    loggedOut() {
      this.authStatus = false;
      this.username = "";
      return this.authStatus
    },
  },
});
