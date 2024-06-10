<template>
  <div class="blank-block"></div>
  <div id="app">
    <nav>
      <div class="card-container">
      <div class="card">
        <router-link to="/">
          <div class="card-content">首页</div>
        </router-link>
      </div>

      <div class="card">
        <router-link to="/course-evaluation">
          <div class="card-content">课程评价</div>
        </router-link>
      </div>

      <div class="card">
        <router-link to="/teacher-evaluation">
          <div class="card-content">教师评价</div>
        </router-link>
      </div>
    </div>

      <!-- <div class="rounded-box">
        <router-link to="/">Home</router-link>
      </div>
      <div class="rounded-box">
      <router-link to="/course-evaluation">课程评价</router-link>
      </div>
      <div class="rounded-box">
      <router-link to="/teacher-evaluation">教师评价</router-link>
      </div> -->
      <!-- <router-link to="/login">登录</router-link>
      <router-link to="/register">注册</router-link> -->
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


<style scoped>
.blank-block {
  height: 20px;
}

.card-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.card {
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 120px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-color 0.2s;
}

.card:hover {
  background-color: #d0d0d0;
}

.card a {
  color: #333;
  text-decoration: none;
  font-size: 1.2rem;
}

.card a.router-link-exact-active {
  color: #20965f;
  font-weight: bold;
}

.card-content {
  text-align: center;
}
</style>
