<template>
  <div class="search-container">
    <!-- Search bar -->
    <v-text-field
      v-model="query"
      label="按回车键搜索"
      outlined
      dense
      @keyup.enter="performSearch"
      class="search-input"
    />

    <!-- Loading message -->
    <v-progress-linear v-if="loading" indeterminate color="primary" class="my-4"></v-progress-linear>

    <!-- Results or No Results message -->
    <v-container v-if="results.length > 0" class="results-container">

      <!-- Data Table -->
      <v-data-table
        :items="results"
        class="elevation-1"
        dense
      >
        <template v-slot:body="{ items }">
          <tr v-for="item in items" :key="item.id">

            <!-- Image -->
            <td>
              <v-img
                :src="item.image"
                alt="Image"
                style="height: 100px; width: 100px; object-fit: cover; margin-right: 30px;"
              ></v-img>
            </td>

            <!-- Price -->
            <td>
              <v-row
                justify="start"
                align="center"
                class="d-flex"
                style="display: flex; flex-wrap: nowrap; align-items: center; white-space: nowrap; margin-top: -5px; margin-right: 40px;"
              >
                <span style="font-weight: bold; margin-right: 10px;">价格：</span>
                <div class="scrollable-text" style="white-space: nowrap;">
                  {{ item.price }}
                </div>
              </v-row>
            </td>

            <!-- Name -->
            <td>
              <v-row
                justify="start"
                align="center"
                class="d-flex"
                style="display: flex; flex-wrap: nowrap; align-items: center; white-space: nowrap; margin-top: -5px; margin-right: 40px;"
              >
                <span style="font-weight: bold; margin-right: 10px;">商品名称：</span>
                <div class="scrollable-text" style="white-space: nowrap;">
                  {{ item.name }}
                </div>
              </v-row>
            </td>

            <!-- Platform -->
            <td>
              <v-row
                justify="start"
                align="center"
                class="d-flex"
                style="display: flex; flex-wrap: nowrap; align-items: center; white-space: nowrap; margin-top: -5px; margin-right: 40px;"
              >
                <span style="font-weight: bold; margin-right: 10px;">平台：</span>
                <div class="scrollable-text" style="white-space: nowrap;">
                  {{ item.platform }}
                </div>
              </v-row>
            </td>

            <!-- Class -->
            <td>
              <v-row
                justify="start"
                align="center"
                class="d-flex"
                style="display: flex; flex-wrap: nowrap; align-items: center; white-space: nowrap; margin-top: -5px; margin-right: 40px;"
              >
                <span style="font-weight: bold; margin-right: 10px;">品类：</span>
                <div class="scrollable-text" style="white-space: nowrap;">
                  {{ item.class }}
                </div>
              </v-row>
            </td>

            <!-- Options -->
            <td>
              <v-row
                justify="start"
                align="center"
                class="d-flex"
                style="display: flex; flex-wrap: nowrap; align-items: center; white-space: nowrap; margin-top: -5px; margin-right: 40px;"
              >
                <span style="font-weight: bold; margin-right: 10px;">可选规格：</span>

                <div class="scrollable-text" style="white-space: nowrap;">
                  {{ convertSize(item.size) }}
                </div>
              
              </v-row>
            </td>

            <!-- Options (old) -->
            <!-- <td>
              <v-row
                justify="start"
                align="center"
                class="d-flex"
                style="display: flex; flex-wrap: nowrap; align-items: center; white-space: nowrap; margin-top: -5px; margin-right: 10px;"
              >
                <span style="font-weight: bold; margin-right: 10px;">可选规格：</span>

                <v-list
                  style="width: 150px;  overflow-x: auto; white-space: nowrap; margin-top: 20px; border: 1px solid #ccc; border-radius: 5px;"
                >
                  <v-list-item
                    v-for="(size, index) in item.size"
                    :key="index"
                    style="display: inline-block; width: 100%; white-space: nowrap;"
                  >
                    <span>
                      {{ size }}
                    </span>
                  </v-list-item>
                </v-list>

              </v-row>
            </td> -->

            <!-- Price Graph -->
            <td>
              <v-row
                justify="start"
                align="center"
                class="d-flex"
                style="display: flex; flex-wrap: nowrap; align-items: center; white-space: nowrap; margin-top: -5px; margin-right: 40px;"
              >
                <span style="font-weight: bold; margin-right: 10px;">价格走势：</span>

                <span style="padding: auto; width: 100px;">
                  <Line :options="chartOptions" :data="convertChartData(item.history_price)"/>
                </span>
              </v-row>
            </td>

            <!-- Link -->
            <td>
              <v-btn :href="item.link" target="_blank" color="purple" small>
                商品链接
              </v-btn>
            </td>

            <!-- Subscribe -->
            <td>
              <v-btn @click="Subscribe(item)" color="primary" small>
                降价提醒
              </v-btn>
            </td>

          </tr>
        </template>

        <!-- makes the header disappears -->
        <template v-slot:headers>
          <thread>
            <tr>
              <span style="font-weight: bold; margin-top: 10px; margin-left: 10px;">
                << 左滑查看全部信息
              </span>
            </tr>
          </thread>
        </template>

      </v-data-table>
    </v-container>

    <!-- No results found -->
    <div
      v-else-if="results.length === 0 && !loading && inited && !error"
      class="no-results-message"
    >
      没有查询到相关结果
    </div>

    <!-- Error message -->
    <transition name="fade">
      <v-alert v-if="error" type="error" class="my-4">
        网络加载错误
      </v-alert>
    </transition>

    <!-- success notification -->
    <transition name="fade" @before-enter="beforeEnter" @after-leave="afterLeave">
      <div v-if="successMessage" class="notification success">
        {{ successMessage }}
      </div>
    </transition>

    <!-- failure notification -->
    <transition name="fade" @before-enter="beforeEnter" @after-leave="afterLeave">
      <div v-if="failureMessage" class="notification failure">
        {{ failureMessage }}
      </div>
    </transition>

  </div>
</template>

<script>
import { postapi } from "../utils/http.js"; // Adjust the import as necessary

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
} from 'chart.js'

import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
)

export default {

  components: {
    Line
  },

  data() {
    return {
      query: "",
      results: [],
      loading: false,
      error: false,
      inited: false,
      failureMessage: '',
      successMessage: '',
      chartOptions: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          x: {
            display: false, // Hide x-axis
          },
          y: {
            display: false, // Hide y-axis
          },
        },
      },
    };
  },

  methods: {

    convertSize(list_of_size) {

      let ret = '';
      for (let i = 0; i < list_of_size.length; i++) {
        if (i > 0) {
          ret += ' ';
        } 
        ret += list_of_size[i];
      }
      return ret;
    },

    convertChartData(price_history) {
      console.log(price_history)
      const data = {
        labels: [],
        datasets: [
          {
            data: [],
          },
        ],
      };
      for (let i = 0; i < price_history.length; i++) {
        data.labels.push(price_history[i][0]);
        data.datasets[0].data.push(price_history[i][1]);
      };
      return data
    },

    async Subscribe(item) {
      const email = localStorage.getItem('email_addr')
      const username = localStorage.getItem('user_name')

      // console.log('here')
      const link = item.link;
      const price = item.price;
      const platform = item.platform;

      const data = { email, platform, link, price, username }

      try {
        const response = await postapi('/api/user/subscribe', data);

        console.log(response)

        if (!response.data.success) {

          this.failureMessage = '订阅失败';
          setTimeout(() => {
            this.failureMessage = '';
          }, 3000);

        } else {

          this.successMessage = '订阅成功';
          setTimeout(() => {
            this.successMessage = '';
          }, 3000);

        }

      } catch (error) {

        console.log('here');
        this.failureMessage = '订阅失败，请检查联网情况';
        setTimeout(() => {
            this.failureMessage = '';
          }, 3000);

      }
    },

    redirectLink(url) {
      window.location.href = url; // Redirects to the specified link
    },

    async performSearch() {
      if (!this.query.trim()) return;

      this.inited = true;
      this.loading = true;
      this.error = false;
      this.results = [];

      const maxRetries = 5;
      const retryInterval = 2000; // 2 seconds

      for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
          const response = await postapi("/api/user/search", { query: this.query });
          this.results = response.data.results;
          return; // If the request is successful, exit the function
        } catch (err) {
          console.error(`Attempt ${attempt} failed:`, err);
          this.error = true;

          if (attempt < maxRetries) {
            console.log(`Retrying in ${retryInterval / 1000} seconds...`);
            await new Promise(resolve => setTimeout(resolve, retryInterval)); // Wait for 2 seconds
          }
        } finally {
          this.loading = false;
        }
      }

      // If all attempts fail, you can perform additional actions here.
      this.error = true; // You can keep the error flag or display a message to the user
      setTimeout(() => {
        this.error = false; // Reset error flag after 1 second
      }, 1000);
    }

  },
};
</script>

<style scoped>
.search-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.search-input {
  width: 100%;
  max-width: 600px;
}

.results-container {
  margin-top: 20px;
  width: 100%;
  overflow-x: auto;
  white-space: nowrap;
}

.scrollable-text {
  width: 80px; /* or any desired width */
  overflow-x: auto; /* enables horizontal scrolling */
  white-space: nowrap; /* prevents text from wrapping to the next line */
}

.error {
  color: red; /* Makes the text red */
  font-size: 12px; /* Optional: Makes the font smaller for error messages */
}

/* Base notification style */
.notification {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #4CAF50; /* Green */
  color: white;
  padding: 15px 25px;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  opacity: 1;
  transition: opacity 0.5s ease-in-out;
  max-width: 90%;
  word-wrap: break-word;
}

/* Adding icon to the notification */
.notification.success {
  background-color: #4CAF50; /* Green */
}

.notification.failure {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.notification .icon {
  margin-right: 10px;
  font-size: 20px;
}

/* Success icon */
.notification.success .icon {
  content: '\u2714'; /* Checkmark icon */
}

/* Fading transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
