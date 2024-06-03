<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/course-evaluation">课程评价</router-link>
      <router-link to="/teacher-evaluation">教师评价</router-link>
      <router-link to="/login">登录</router-link>
      <router-link to="/register">注册</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
  //
</script>

<style>
nav {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

router-link {
  text-decoration: none;
  color: #42b983;
}

router-link-active {
  font-weight: bold;
}
</style>
