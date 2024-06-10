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
          status: '已选',
          reviews: [
            [5,"Engaging discussions on the intricacies of human behavior enhance understanding."],
            [3,"Overlapping content in lectures and readings can lead to redundancy."],
            [4,"Practical applications of psychological theories enrich the learning experience."]
          ]
        },
        { id: 2, 
          code: '2110860', 
          name: '科研实践 I', 
          credits: '2.0', 
          category: '专业课', 
          department: '计算机科学与技术学院', 
          status: '未选',
          reviews: [
    [4, "Comprehensive coverage of networking concepts with real-world examples."],
    [2, "Some topics are outdated and need refreshing to match current technologies."],
    [5, "Lab sessions are highly practical and beneficial for understanding complex concepts."]
          ]
        },
        { id: 3, 
          code: '2110870', 
          name: '科研实践 II', 
          credits: '4.0', 
          category: '专业课', 
          department: '计算机科学与技术学院', 
          status: '未选',
          "reviews": [
    [5, "Fascinating insights into AI developments and future possibilities."],
    [4, "Combination of theory and practical projects is well balanced."],
    [3, "Course pacing can be fast, requiring additional self-study."]
          ]
        },
        { id: 4, 
          code: '2119070', 
          name: '计算机前沿技术讲座', 
          credits: '1.0', 
          category: '专业课', 
          department: '计算机科学与技术学院', 
          status: '未选',
          "reviews": [
    [4, "In-depth analysis of OS concepts with hands-on lab work."],
    [3, "Some sections are dense and challenging to follow."],
    [5, "Excellent resources and support from the instructor."]
          ]
        },
        { id: 5, 
          code: '2119134', 
          name: '数字媒体后期制作', 
          credits: '2.0', 
          category: '专业课', 
          department: '计算机科学与技术学院', 
          status: '未选',
          "reviews": [
  [5, "Well-structured course with clear and engaging lectures."],
  [4, "Relevant case studies make the theoretical concepts relatable."],
  [3, "The workload can be overwhelming at times."]
          ]
        },
        { id: 6, 
          code: '2222222', 
          name: '生命探索', 
          credits: '2.0', 
          category: '通识必修课程', 
          department: '生命科学学院', 
          status: '未选',
          reviews:[ 
  [3, "Theoretical focus with less emphasis on practical implementation."],
  [4, "Detailed exploration of SQL and NoSQL databases enhances learning."],
  [3, "Assignments are challenging but valuable for deepening understanding."]
          ]  
        },
        {
          "id": 7,
          "code": "2110930",
          "name": "高级算法设计",
          "credits": "3.0",
          "category": "专业课",
          "department": "计算机科学与技术学院",
          "status": "未选",
          "reviews": [
  [4, "Insightful discussions and well-organized materials."],
  [2, "Some topics need more detailed explanations."],
  [5, "Interactive sessions greatly enhance understanding."]
          ]
        },
        {
          "id": 8,
          "code": "2111031",
          "name": "人工智能导论",
          "credits": "3.0",
          "category": "专业课",
          "department": "计算机科学与技术学院",
          "status": "已选",
          "reviews": [
  [5, "Comprehensive overview of key concepts in the field."],
  [3, "Some assignments are too time-consuming."],
  [4, "Useful feedback from the instructor."]
          ]
        },
        {
          "id": 9,
          "code": "2112045",
          "name": "大数据分析与处理",
          "credits": "3.0",
          "category": "专业课",
          "department": "计算机科学与技术学院",
          "status": "未选",
          "reviews": [
  [3, "The course content is somewhat outdated."],
  [4, "Good mix of lectures and practical exercises."],
  [5, "Supportive learning environment and helpful resources."]
          ]
        },
        {
          "id": 10,
          "code": "2112046",
          "name": "云计算与大数据技术",
          "credits": "3.0",
          "category": "专业课",
          "department": "计算机科学与技术学院",
          "status": "未选",
          "reviews": [
  [5, "The course is very informative and well-paced."],
  [4, "Real-world examples make the material more engaging."],
  [3, "The exam was challenging but fair."]
          ]
        },
        {
          "id": 11,
          "code": "1130145",
          "name": "马克思主义基本原理",
          "credits": "3.0",
          "category": "通识必修课程",
          "department": "马克思主义学院",
          "status": "未选",
          "reviews": [
  [4, "Detailed explanations of complex topics."],
  [3, "Some lectures are difficult to follow without prior knowledge."],
  [5, "Excellent use of multimedia resources."]
          ]
        },
        {
          "id": 12,
          "code": "1100113",
          "name": "大学英语（综合）",
          "credits": "4.0",
          "category": "通识必修课程",
          "department": "外国语学院",
          "status": "已选",
          "reviews": [
  [5, "Engaging lectures with practical applications."],
  [4, "Instructor is very knowledgeable and approachable."],
  [3, "The reading materials could be more up-to-date."]
          ]
        },
        {
          "id": 13,
          "code": "2220011",
          "name": "大学篮球",
          "credits": "1.0",
          "category": "体育课程",
          "department": "体育与健康学院",
          "status": "已选",
          "reviews": [
  [4, "Thorough coverage of the subject matter."],
  [3, "More hands-on practice would be beneficial."],
  [5, "Great course for anyone interested in this field."]
          ]
        },
        {
          "id": 14,
          "code": "2220022",
          "name": "游泳基础",
          "credits": "1.0",
          "category": "体育课程",
          "department": "体育与健康学院",
          "status": "未选",
          "reviews": [
  [5, "Very well-organized and informative."],
  [4, "Assignments are challenging but help deepen understanding."],
  [3, "Some topics are not explained in enough detail."]
          ]
        },
        {
          "id": 15,
          "code": "2220033",
          "name": "瑜伽与健身",
          "credits": "1.0",
          "category": "体育课程",
          "department": "体育与健康学院",
          "status": "未选",
          "reviews": [
  [4, "Good balance of theory and practical work."],
  [3, "The pace of the course is quite fast."],
  [5, "Instructor is excellent and very supportive."]
          ]
        },
        {
          "id": 16,
          "code": "3220044",
          "name": "创业与创新管理",
          "credits": "3.0",
          "category": "跨类(专业)",
          "department": "经济管理学院",
          "status": "已选",
          "reviews": [
  [5, "Comprehensive and well-explained content."],
  [4, "Interactive sessions help clarify complex ideas."],
  [3, "Occasional technical difficulties during online lectures."]
          ]
        },
        {
          "id": 17,
          "code": "3220055",
          "name": "文化创意产业",
          "credits": "3.0",
          "category": "跨类(专业)",
          "department": "经济管理学院",
          "status": "未选",
          "reviews": [
  [4, "Instructor provides real-world examples to aid understanding."],
  [2, "Some topics are covered too briefly."],
  [5, "Excellent course structure and pacing."]
          ]
        },
        {
          "id": 18,
          "code": "3220066",
          "name": "艺术与社会",
          "credits": "3.0",
          "category": "跨类(专业)",
          "department": "艺术与设计学院",
          "status": "未选",
          "reviews": [
  [5, "The assignments are practical and relevant."],
  [4, "Lectures are engaging and informative."],
  [3, "Additional reading materials would be helpful."]
          ]
        },
        {
          "id": 19,
          "code": "4110022",
          "name": "离散数学",
          "credits": "4.0",
          "category": "专业基础课程",
          "department": "计算机科学与技术学院",
          "status": "已选",
          "reviews": [
  [3, "The course could benefit from more visual aids."],
  [4, "Discussions and group work enhance learning."],
  [5, "Very knowledgeable and approachable instructor."]
          ]
        },
        {
          "id": 20,
          "code": "4110033",
          "name": "数据结构与算法",
          "credits": "4.0",
          "category": "专业基础课程",
          "department": "计算机科学与技术学院",
          "status": "已选",
          "reviews": [
  [5, "Course content is up-to-date and well-researched."],
  [4, "Interactive tools used in lectures are very helpful."],
  [3, "The final project is quite demanding."]
          ]
        },
        {
          "id": 21,
          "code": "4110044",
          "name": "计算机网络",
          "credits": "3.0",
          "category": "专业基础课程",
          "department": "计算机科学与技术学院",
          "status": "未选",
          "reviews": [
  [4, "Good balance between theory and practice."],
  [3, "Some lectures are too fast-paced."],
  [5, "The instructor is very supportive and provides great feedback."]
          ]
        },
        {
          "id": 22,
          "code": "5110111",
          "name": "创新创业竞赛",
          "credits": "2.0",
          "category": "认定型课程",
          "department": "创新与创业中心",
          "status": "已选",
          "reviews": [
  [5, "Course provides a deep understanding of the subject."],
  [4, "Real-life case studies are very insightful."],
  [3, "More examples during lectures would be beneficial."]
          ]
        },
        {
          "id": 23,
          "code": "5110122",
          "name": "社会实践",
          "credits": "2.0",
          "category": "认定型课程",
          "department": "社会服务与实践中心",
          "status": "未选",
          "reviews": [
  [4, "Well-structured and easy to follow."],
  [2, "Some topics are covered too superficially."],
  [5, "The instructor is very engaging and knowledgeable."]
          ]
        },
        {
          "id": 24,
          "code": "5110133",
          "name": "学科竞赛",
          "credits": "3.0",
          "category": "认定型课程",
          "department": "学术竞赛中心",
          "status": "未选",
          "reviews": [
  [5, "Practical exercises are very useful."],
  [4, "Lectures are clear and concise."],
  [3, "More detailed explanations of complex concepts are needed."]
          ]
        },
        {
          "id": 25,
          "code": "6110144",
          "name": "国际商务",
          "credits": "3.0",
          "category": "国际化课程",
          "department": "经济管理学院",
          "status": "已选",
          "reviews": [
  [3, "Course materials could be more organized."],
  [4, "Hands-on projects help solidify understanding."],
  [5, "Excellent support from the teaching team."]
          ]
        },
        {
          "id": 26,
          "code": "6110155",
          "name": "全球化与世界经济",
          "credits": "3.0",
          "category": "国际化课程",
          "department": "经济管理学院",
          "status": "未选",
          "reviews": [
  [5, "Course is very well-organized and thorough."],
  [4, "Instructor provides useful real-world applications."],
  [3, "Some readings are quite dense."]
          ]
        },
        {
          "id": 27,
          "code": "6110166",
          "name": "跨文化交流",
          "credits": "2.0",
          "category": "国际化课程",
          "department": "外国语学院",
          "status": "未选",
          "reviews": [
  [4, "Course provides a good foundational understanding."],
  [3, "More practical examples during lectures would help."],
  [5, "Instructor is very knowledgeable and approachable."]
          ]
        },
        {
          "id": 28,
          "code": "7110171",
          "name": "计算机网络实验",
          "credits": "2.0",
          "category": "实验课程",
          "department": "计算机科学与技术学院",
          "status": "已选",
          "reviews": [
  [5, "Assignments are challenging but rewarding."],
  [4, "Lectures are very informative."],
  [3, "The pace of the course is a bit too fast."]
          ]
        },
        {
          "id": 29,
          "code": "7110182",
          "name": "操作系统实验",
          "credits": "2.0",
          "category": "实验课程",
          "department": "计算机科学与技术学院",
          "status": "未选",
          "reviews": [
  [4, "Good integration of theory and practical applications."],
  [3, "Some topics are difficult to grasp initially."],
  [5, "The instructor is excellent and very helpful."]
          ]
        },
        {
          "id": 30,
          "code": "7110193",
          "name": "人工智能实验",
          "credits": "2.0",
          "category": "实验课程",
          "department": "计算机科学与技术学院",
          "status": "未选",
          "reviews": [
  [5, "Well-structured with clear and engaging lectures."],
  [4, "Relevant case studies are used throughout."],
  [3, "The workload can be heavy at times."]
          ]
        },
        {
          "id": 31,
          "code": "8110204",
          "name": "高级计算理论",
          "credits": "3.0",
          "category": "荣誉课程",
          "department": "计算机科学与技术学院",
          "status": "未选",
          "reviews": [
  [4, "Insightful and well-organized materials."],
  [2, "Some lectures need more detailed explanations."],
  [5, "Interactive sessions greatly enhance learning."]
          ]
        },
        {
          "id": 32,
          "code": "8110215",
          "name": "高级数据科学",
          "credits": "3.0",
          "category": "荣誉课程",
          "department": "计算机科学与技术学院",
          "status": "已选",
          "reviews": [
  [5, "Comprehensive overview of key concepts."],
  [3, "Some assignments are very time-consuming."],
  [4, "Useful feedback from the instructor."]
          ]
        },
        {
          "id": 33,
          "code": "8110226",
          "name": "高级人工智能",
          "credits": "3.0",
          "category": "荣誉课程",
          "department": "计算机科学与技术学院",
          "status": "未选",
          "reviews": [
  [3, "Some content is a bit outdated."],
  [4, "Good mix of lectures and practical exercises."],
  [5, "Supportive learning environment and helpful resources."]
          ]
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
