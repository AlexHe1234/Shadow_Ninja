<template>
    <div class="search-bar border-box">
      <input type="text" v-model="query" @input="onInput" placeholder="搜索教师名字" />
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        query: ''
      };
    },
    methods: {
      onInput() {
        this.$emit('search', this.query);
      }
    }
  };
  </script>
  
  <style scoped>
  .search-bar {
    display: inline-block;
    min-width: 800px;
  }
  
  input {
    padding: 10px;
    min-width: 800px;
    width: 100%;
    font-size: 16px;
    border: 1px solid #007BFF;
    border-radius: 5px;
  }
  </style>
  