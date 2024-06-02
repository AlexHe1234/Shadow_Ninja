<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-text-field
          v-model="searchTerm"
          label="搜索课程"
          single-line
          hide-details
          @input="searchCourses"
        ></v-text-field>
        <v-tabs
          v-model="activeTab"
          background-color="blue-grey lighten-5"
          fixed-tabs
          @change="searchCourses" 
        >
          <v-tab v-for="(category, index) in categories" :key="index">
            {{ category }}
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="activeTab">
          
            <v-card flat>
              <v-card-text>
                <v-list>
                  <v-list-item-group>
                    <v-list-item v-for="course in filteredCourses" :key="course.id">
                      <v-list-item-content>
                        <v-list-item-title>{{ course.name }}</v-list-item-title>
                        <v-list-item-subtitle>{{ course.department }} - {{ course.credits }} 学分</v-list-item-subtitle>
                      </v-list-item-content>
                      <v-list-item-action>
                        <v-chip :color="courseStatusColor(course.status)">{{ course.status }}</v-chip>
                      </v-list-item-action>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-card-text>
            </v-card>
          
        </v-tabs-items>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'CourseEvaluation',
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
        { id: 6, code: '222222', name: '测试课程', credits: '2.0', category: '通识必修课程', department: '计算机科学与技术学院', status: '未选' }
      ],
      filteredCourses: []
    };
  },
  methods: {
  searchCourses() {
    this.filteredCourses = [];  // 清空之前的搜索结果
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
  courseStatusColor(status) {
    switch (status) {
      case '已选':
        return 'yellow lighten-3';
      case '未选':
        return 'blue lighten-4';
      default:
        return 'grey lighten-2';
    }
  }
},
    mounted() {
    this.searchCourses();  // 在组件加载后进行一次全局搜索初始化
    },
    watch: {
    activeTab() {
        this.searchCourses();  // 当标签页变更时重新搜索
    },
    searchTerm() {
        this.searchCourses();  // 当搜索词变更时重新搜索
    }
    }

};
</script>

<style scoped>
.v-card {
  transition: background-color 0.3s ease;
}
</style>
