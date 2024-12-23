<template>
  <div>
    <!-- Logo image fixed to the top-left corner -->
    <div class="logo-container">
      <img src="@/assets/images/logo.png" alt="ShopSmart Logo" class="logo-image" />
    </div>
    
    <!-- Main content of the page -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style scoped>
.logo-container {
  position: fixed;  /* Keeps the logo fixed in position */
  top: 20px;        /* Distance from the top of the page */
  left: 20px;       /* Distance from the left of the page */
  z-index: 10;      /* Ensures the logo stays above other content */
}

.logo-image {
  width: 100px;      /* You can adjust the width of the logo */
  height: auto;      /* Maintains aspect ratio */
}
</style>
