<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        
        <!-- 当searchTerm变化时触发searchCourses方法 -->
        <v-text-field v-model="searchTerm" label="搜索课程" single-line hide-details @input="searchCourses"></v-text-field> 
        
        <!-- 搜索框键入时，备选选项卡组件；当searchCourses方法被触发时，选项卡组件会被重新渲染 -->
        <v-tabs v-model="activeTab" background-color="blue-grey lighten-5" fixed-tabs @change="searchCourses">
          <!-- 使用v-for指令遍历categories数组，为每个选项卡绑定点击事件；当用户点击一个标签时，它会更新 activeTab 的值为被点击的标签的索引 -->
          <v-tab v-for="(category, index) in categories" :key="index" :class="{ 'active-tab': activeTab === index }"
            @click="activeTab = index">
            {{ category }}
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="activeTab">
          <v-card flat>
            <v-card-text>
              <v-list>
                <v-list-item-group>
                  <v-list-item v-for="course in filteredCourses" :key="course.id"
                    :class="{ 'selected-item': selectedCourse && selectedCourse.id === course.id }" outlined
                    @click="selectCourse(course)">
                    <v-list-item-content>
                      <v-list-item-title>{{ course.name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ course.department }} - {{ course.credits }} 学分</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-card-text>
          </v-card>
        </v-tabs-items>
      
      </v-col>
    </v-row>
    <v-row v-if="selectedCourse">
      <v-col>
        <CourseDetail :course="selectedCourse" @add-review="addReview" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CourseDetail from './CourseDetail.vue';

export default {
  name: 'CourseEvaluation',
  components: {
    CourseDetail
  },
  data() {
    return {
      activeTab: 0,
      searchTerm: '',
      categories: ['专业课', '通识必修课程', '体育课程', '跨类(专业)', '专业基础课程', '认定型课程', '国际化课程', '实验课程', '荣誉课程'],
      courses: [
        {
          id: 1,
          code: '2110721',
          name: '工程实践',
          credits: '3.0',
          category: '专业课',
          department: '计算机科学与技术学院',
          reviews: [
            [5,"Engaging discussions on the intricacies of human behavior enhance understanding."],
            [3,"Overlapping content in lectures and readings can lead to redundancy."],
            [4,"Practical applications of psychological theories enrich the learning experience."]
          ]
        },
      ],
      filteredCourses: [],
      selectedCourse: null
    };
  },
  methods: {
    searchCourses() {
      this.filteredCourses = [];
      if (this.searchTerm) {
        this.filteredCourses = this.courses.filter(course =>
          course.name.toLowerCase().includes(this.searchTerm.toLowerCase()) &&
          course.category === this.categories[this.activeTab]
        );
      } else {
        this.filteredCourses = this.courses.filter(course =>
          course.category === this.categories[this.activeTab]
        );
      }
    },

    selectCourse(course) {
      console.log("Click detected, course:", course); // 检查点击是否触发
      this.selectedCourse = course;
      console.log("Selected course set:", this.selectedCourse); // 确认selectedCourse被正确设置
    },

    addReview(courseId, review) {
      const course = this.courses.find(c => c.id === courseId);
      if (course) {
        course.reviews.push(review);
        // Update the course rating based on the new review
        course.rating = (course.rating * (course.reviews.length - 1) + review.rating) / course.reviews.length;
      }
    }
  },
  mounted() {
    this.searchCourses();
  },
  watch: {
    activeTab() {
      this.searchCourses();
    },
    searchTerm() {
      this.searchCourses();
    }
  }
};
</script>



<style scoped>
.selected-item {
  transition: background-color 0.3s ease;
  /* 添加平滑的过渡效果 */
  background-color: rgb(255, 255, 255);
}
.active-tab {
  background-color: rgb(88, 129, 87) !important; /* 确保此样式优先级更高 */
  color: white; /* 设置文字颜色 */
}
.v-card {

  transition: background-color 0.3s ease;
}
</style>
