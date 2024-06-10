<template>
  <v-card>
    <v-card-title>
      <span class="headline">{{ course.name }}</span>
    </v-card-title>
    <v-card-text>
      <p>课程代码: {{ course.code }}</p>
      <p>学分: {{ course.credits }}</p>
      <p>所属学院: {{ course.department }}</p>
      <p v-if="course.rating !== undefined">评分: {{ course.rating.toFixed(1) }} / 5.0</p>
      <p v-else>评分: 暂无</p>
      <v-divider></v-divider>
      <v-subheader>评论</v-subheader>
      <v-list>
        <v-list-item v-for="(review, index) in course.reviews" :key="index">
          <v-list-item-content>
            <v-list-item-title>评分: {{ review.rating }} / 5</v-list-item-title>
            <v-list-item-subtitle>{{ review.comment }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-text-field v-model="newComment" label="输入评价" outlined></v-text-field>
      <v-rating v-model="newRating" max="5" half-increments></v-rating>
      <v-btn color="primary" @click="submitReview">提交</v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'CourseDetail',
  props: {
    course: Object
  },
  data() {
    return {
      newComment: '',
      newRating: 0
    };
  },
  methods: {
    submitReview() {
      if (this.newComment && this.newRating) {
        this.$emit('add-review', this.course.id, {
          rating: this.newRating,
          comment: this.newComment
        });
        this.newComment = '';
        this.newRating = 0;
      } else {
        alert("请填写完整的评论和评分！");
      }
    }
  }
};
</script>
