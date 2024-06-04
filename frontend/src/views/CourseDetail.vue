<template>
    <div class="course-detail border-box">
      <h2>{{ course.name }}</h2>
      <p>{{ course.department }} - {{ course.credits }} 学分</p>
      <div v-if="course.ratings.length > 0">
        <h3>评分:</h3>
        <v-rating
          :value="course.rating"
          color="amber"
          dense
          half-increments
          readonly
          size="24"
        ></v-rating>
        <span>({{ course.ratings.length }} 个评分)</span>
      </div>
      <div v-if="course.reviews.length > 0">
        <h3>评论:</h3>
        <v-list>
          <v-list-item v-for="(review, index) in course.reviews" :key="index">
            <v-list-item-content>
              <v-list-item-title>{{ review.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ review.text }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </div>
      <div v-else>
        <p>暂无评论</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      course: {
        type: Object,
        required: true
      }
    },
    computed: {
  courseRating() {
    const { course } = this;
    if (course.ratings.length > 0) {
      return course.ratings.reduce((total, rating) => total + rating, 0) / course.ratings.length;
    } else {
      return 0;
    }
  }
  }
  }
  </script>
  
  <style scoped>
  .course-detail {
    margin-top: 20px;
    padding: 20px;
  }
  </style>