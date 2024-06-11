<template>
  <!-- <h1 class="centered-title">智能教师评价系统</h1> -->
  <SearchBar @search="handleSearch" />
  <TeacherList
    :teachers="filteredTeachers"
    @select="handleSelect"
    v-if="filteredTeachers.length > 0 && !selectedTeacher"
  />
  <TeacherDetail
    :teacher="selectedTeacher"
    v-if="selectedTeacher"
    @back="handleBack"
  />
</template>
<script>
import SearchBar from './SearchBar.vue';
import TeacherList from './TeacherList.vue';
import TeacherDetail from './TeacherDetail.vue';

export default {
components: {
  SearchBar,
  TeacherList,
  TeacherDetail
},
data() {
  return {
    teachers: [
      { id: 1, name: '张三', subject: '数学', rating: 4.5, reviews: [], ratings: [] },
      { id: 2, name: '李四', subject: '英语', rating: 4.0, reviews: [], ratings: [] },
      { id: 3, name: '王五', subject: '物理', rating: 4.2, reviews: [], ratings: [] },
      { id: 4, name: '赵六', subject: '化学', rating: 3.8, reviews: [], ratings: [] },
      { id: 5, name: '刘七', subject: '历史', rating: 4.1, reviews: [], ratings: [] },  
      { id: 6, name: '孙八', subject: '计算机', rating: 4.4, reviews: [], ratings: [] },
    { id: 7, name: '周九', subject: '生物', rating: 3.9, reviews: [], ratings: [] },
    { id: 8, name: '吴十', subject: '经济学', rating: 4.3, reviews: [], ratings: [] },
    { id: 9, name: '郑十一', subject: '艺术', rating: 4.0, reviews: [], ratings: [] },
    { id: 10, name: '马十二', subject: '音乐', rating: 4.2, reviews: [], ratings: [] },
    { id: 11, name: '钱十三', subject: '哲学', rating: 3.7, reviews: [], ratings: [] },
    { id: 12, name: '陈十四', subject: '心理学', rating: 4.1, reviews: [], ratings: [] },
    { id: 13, name: '朱十五', subject: '建筑学', rating: 4.0, reviews: [], ratings: [] },
    { id: 14, name: '蒋十六', subject: '医学', rating: 4.4, reviews: [], ratings: [] },
    { id: 15, name: '沈十七', subject: '法学', rating: 3.9, reviews: [], ratings: [] },
    { id: 16, name: '韩十八', subject: '管理学', rating: 4.2, reviews: [], ratings: [] },
    { id: 17, name: '曹十九', subject: '教育学', rating: 4.0, reviews: [], ratings: [] },
    { id: 18, name: '杜二十', subject: '语言学', rating: 4.1, reviews: [], ratings: [] },
    { id: 19, name: '魏二十一', subject: '体育', rating: 4.3, reviews: [], ratings: [] },
    { id: 20, name: '毛二十二', subject: '地理', rating: 4.0, reviews: [], ratings: [] },

    ],
    filteredTeachers: [],
    selectedTeacher: null
  };
},
methods: {
  handleSearch(query) {
    this.filteredTeachers = this.teachers.filter(teacher =>
      teacher.name.includes(query)
    );
  },
  handleSelect(teacher) {
    this.selectedTeacher = teacher;
  },
  handleBack() {
    this.selectedTeacher = null;
  }
}
};
</script>

<style>
#app {
font-family: Avenir, Helvetica, Arial, sans-serif;
text-align: center;
margin-top: 20px;
}

.border-box {
border: 1px solid #ccc;
padding: 10px;
margin: 10px;
border-radius: 5px;
}

input, textarea, select, button {
border: 1px solid #007BFF;
padding: 10px;
margin: 10px;
border-radius: 5px;
}

button {
background-color: #007BFF;
color: white;
cursor: pointer;
transition: background-color 0.3s;
}

button:hover {
background-color: #0056b3;
}

.teacher-detail {
margin-top: 20px;
}
</style>
