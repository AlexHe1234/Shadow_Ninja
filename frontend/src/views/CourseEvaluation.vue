<template>
  <h1 class="centered-title">智能课程评价系统</h1>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-text-field v-model="searchTerm" label="搜索课程" single-line hide-details @input="searchCourses"></v-text-field>
        <v-tabs v-model="activeTab" background-color="blue-grey lighten-5" fixed-tabs @change="searchCourses">
          <v-tab v-for="(category, index) in categories" :key="index">
            {{ category }}
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="activeTab">
          <v-card flat>
            <v-card-text>
              <v-list>
                <v-list-item-group>
                  <v-list-item v-for="course in filteredCourses" :key="course.id" outlined
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
        { id: 1, code: '2110721', name: '工程实践', credits: '3.0', category: '专业课', department: '计算机科学与技术学院', status: '已选' },
        { id: 2, code: '2110860', name: '科研实践 I', credits: '2.0', category: '专业课', department: '计算机科学与技术学院', status: '未选' },
        { id: 3, code: '2110870', name: '科研实践 II', credits: '4.0', category: '专业课', department: '计算机科学与技术学院', status: '未选' },
        { id: 4, code: '2119070', name: '计算机前沿技术讲座', credits: '1.0', category: '专业课', department: '计算机科学与技术学院', status: '未选' },
        { id: 5, code: '21191340', name: '数字媒体后期制作', credits: '2.0', category: '专业课', department: '计算机科学与技术学院', status: '未选' },
        { id: 6, code: '222222', name: '生命探索', credits: '2.0', category: '通识必修课程', department: '生命科学学院', status: '未选' },
        {
          "id": 7,
          "code": "2110930",
          "name": "高级算法设计",
          "credits": "3.0",
          "category": "专业课",
          "department": "计算机科学与技术学院",
          "status": "未选"
        },
        {
          "id": 8,
          "code": "2111031",
          "name": "人工智能导论",
          "credits": "3.0",
          "category": "专业课",
          "department": "计算机科学与技术学院",
          "status": "已选"
        },
        {
          "id": 9,
          "code": "2112045",
          "name": "大数据分析与处理",
          "credits": "3.0",
          "category": "专业课",
          "department": "计算机科学与技术学院",
          "status": "未选"
        },
        {
          "id": 10,

          "code": "2112046",
          "name": "云计算与大数据技术",
          "credits": "3.0",
          "category": "专业课",
          "department": "计算机科学与技术学院",
          "status": "未选"
        },
        {
          "id": 10,
          "code": "1130120",
          "name": "中国近现代史纲要",
          "credits": "2.0",
          "category": "通识必修课程",
          "department": "马克思主义学院",
          "status": "已选"
        },
        {
          "id": 11,
          "code": "1130145",
          "name": "马克思主义基本原理",
          "credits": "3.0",
          "category": "通识必修课程",
          "department": "马克思主义学院",
          "status": "未选"
        },
        {
          "id": 12,
          "code": "1100113",
          "name": "大学英语（综合）",
          "credits": "4.0",
          "category": "通识必修课程",
          "department": "外国语学院",
          "status": "已选"
        },
        {
          "id": 13,
          "code": "2220011",
          "name": "大学篮球",
          "credits": "1.0",
          "category": "体育课程",
          "department": "体育与健康学院",
          "status": "已选"
        },
        {
          "id": 14,
          "code": "2220022",
          "name": "游泳基础",
          "credits": "1.0",
          "category": "体育课程",
          "department": "体育与健康学院",
          "status": "未选"
        },
        {
          "id": 15,
          "code": "2220033",
          "name": "瑜伽与健身",
          "credits": "1.0",
          "category": "体育课程",
          "department": "体育与健康学院",
          "status": "未选"
        },
        {
          "id": 16,
          "code": "3220044",
          "name": "创业与创新管理",
          "credits": "3.0",
          "category": "跨类(专业)",
          "department": "经济管理学院",
          "status": "已选"
        },
        {
          "id": 17,
          "code": "3220055",
          "name": "文化创意产业",
          "credits": "3.0",
          "category": "跨类(专业)",
          "department": "经济管理学院",
          "status": "未选"
        },
        {
          "id": 18,
          "code": "3220066",
          "name": "艺术与社会",
          "credits": "3.0",
          "category": "跨类(专业)",
          "department": "艺术与设计学院",
          "status": "未选"
        },
        {
          "id": 19,
          "code": "4110022",
          "name": "离散数学",
          "credits": "4.0",
          "category": "专业基础课程",
          "department": "计算机科学与技术学院",
          "status": "已选"
        },
        {
          "id": 20,
          "code": "4110033",
          "name": "数据结构与算法",
          "credits": "4.0",
          "category": "专业基础课程",
          "department": "计算机科学与技术学院",
          "status": "已选"
        },
        {
          "id": 21,
          "code": "4110044",
          "name": "计算机网络",
          "credits": "3.0",
          "category": "专业基础课程",
          "department": "计算机科学与技术学院",
          "status": "未选"
        },
        {
          "id": 22,
          "code": "5110111",
          "name": "创新创业竞赛",
          "credits": "2.0",
          "category": "认定型课程",
          "department": "创新与创业中心",
          "status": "已选"
        },
        {
          "id": 23,
          "code": "5110122",
          "name": "社会实践",
          "credits": "2.0",
          "category": "认定型课程",
          "department": "社会服务与实践中心",
          "status": "未选"
        },
        {
          "id": 24,
          "code": "5110133",
          "name": "学科竞赛",
          "credits": "3.0",
          "category": "认定型课程",
          "department": "学术竞赛中心",
          "status": "未选"
        },
        {
          "id": 25,
          "code": "6110144",
          "name": "国际商务",
          "credits": "3.0",
          "category": "国际化课程",
          "department": "经济管理学院",
          "status": "已选"
        },
        {
          "id": 26,
          "code": "6110155",
          "name": "全球化与世界经济",
          "credits": "3.0",
          "category": "国际化课程",
          "department": "经济管理学院",
          "status": "未选"
        },
        {
          "id": 27,
          "code": "6110166",
          "name": "跨文化交流",
          "credits": "2.0",
          "category": "国际化课程",
          "department": "外国语学院",
          "status": "未选"
        },
        {
          "id": 28,
          "code": "7110171",
          "name": "计算机网络实验",
          "credits": "2.0",
          "category": "实验课程",
          "department": "计算机科学与技术学院",
          "status": "已选"
        },
        {
          "id": 29,
          "code": "7110182",
          "name": "操作系统实验",
          "credits": "2.0",
          "category": "实验课程",
          "department": "计算机科学与技术学院",
          "status": "未选"
        },
        {
          "id": 30,
          "code": "7110193",
          "name": "人工智能实验",
          "credits": "2.0",
          "category": "实验课程",
          "department": "计算机科学与技术学院",
          "status": "未选"
        },
        {
          "id": 31,
          "code": "8110204",
          "name": "高级计算理论",
          "credits": "3.0",
          "category": "荣誉课程",
          "department": "计算机科学与技术学院",
          "status": "未选"
        },
        {
          "id": 32,
          "code": "8110215",
          "name": "高级数据科学",
          "credits": "3.0",
          "category": "荣誉课程",
          "department": "计算机科学与技术学院",
          "status": "已选"
        },
        {
          "id": 33,
          "code": "8110226",
          "name": "高级人工智能",
          "credits": "3.0",
          "category": "荣誉课程",
          "department": "计算机科学与技术学院",
          "status": "未选"
        }
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
.v-card {
  transition: background-color 0.3s ease;
}
</style>
