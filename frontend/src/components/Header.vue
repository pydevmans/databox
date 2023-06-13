<template>
  <div id="header">
    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/features">Features</RouterLink>
      <RouterLink to="/dashboard">Dashboard</RouterLink>
      <!-- <RouterLink to="/dashboard/<database:str>">Database</RouterLink> -->
      <!-- <RouterLink to="/dashboard/<database:str>/query?page=2">Database</RouterLink> -->
      <RouterLink to="/login">Log In</RouterLink>
      <RouterLink to="/signup">Sign Up</RouterLink>
    </nav>
  </div>
</template>

<style scoped>
nav {
  text-align: right;
}

nav>a {
  font-size: larger;
  padding: 0 5px;
}
</style>