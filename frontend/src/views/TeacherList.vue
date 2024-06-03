<template>
    <div class="teacher-list border-box">
      <ul>
        <li v-for="teacher in teachers" :key="teacher.id" @click="selectTeacher(teacher)">
          {{ teacher.name }} - {{ teacher.subject }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: ['teachers'],
    methods: {
      selectTeacher(teacher) {
        this.$emit('select', teacher);
      }
    }
  };
  </script>
  
  <style scoped>
  .teacher-list {
    display: inline-block;
    width: 100%;
    max-width: 800px;
    min-width: 800px;
    margin: 0 auto;
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    padding: 10px;
    border: 1px solid #ccc;
    margin: 5px 0;
    cursor: pointer;
    background-color: #f9f9f9;
    transition: background-color 0.3s;
  }
  
  li:hover {
    background-color: #e9e9e9;
  }
  </style>
  
  
  