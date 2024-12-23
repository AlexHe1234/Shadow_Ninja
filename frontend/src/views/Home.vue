<template>
  <div>

    <!-- Check if the user is logged in -->
    <div v-if="is_login">
      <!-- If logged in, display an image -->
      
      <p>
        yo
      </p>

    </div>

    <div v-else>
      <!-- If not logged in, redirect to the login page -->
      <p>You are not logged in. Redirecting...</p>
    </div>

  </div>
</template>

<script>
</script>

<style scoped>
img {
  max-width: 100%;
  height: auto;
}
</style>
