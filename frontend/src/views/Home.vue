<template>
  <v-app>
    <!-- Navigation Rail (Collapsible List) -->
    <v-navigation-drawer
      v-model="isMenuVisible"
      app
      temporary
      right
      width="200"
    >
      <v-list class="menu-list">
        
        <v-list-item @click="goToSearch" class="item-font">
          全网搜索
        </v-list-item>

        <!-- <v-list-item @click="goToBrowse" class="item-font">
          Browse
        </v-list-item> -->

        <v-list-item @click="logout" class="logout-font">
          注销用户
        </v-list-item>
      
      </v-list>
    </v-navigation-drawer>

    <!-- Toggle Button for Menu -->
    <v-btn
      icon
      @click="toggleMenu"
      class="menu-toggle-btn"
    >
      <v-icon>mdi-menu</v-icon>
    </v-btn>

    <!-- Main Content with Background Image -->
    <v-main>
      <div class="home-page">
        <router-view></router-view>
      </div>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      isMenuVisible: false, // Control the visibility of the menu
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuVisible = !this.isMenuVisible; // Toggle the menu visibility
    },
    goToSearch() {
      this.$router.push({ name: 'Search' });
    },
    goToBrowse() {
      this.$router.push({ name: 'Browse' });
    },
    logout() {
      localStorage.setItem('is_login', 'false');
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>

<style scoped>
/* Optional Custom Styling */
.v-navigation-drawer {
  z-index: 1000;
}

/* Ensure the button stays on top and is positioned correctly */
.menu-toggle-btn {
  background: none;
  box-shadow: none;
  position: fixed;
  top: 3px;
  right: 3px;
  z-index: 1001; /* Ensure the button stays on top */
}

.menu-toggle-btn .v-icon {
  font-size: 25px; /* Optional: adjust icon size */
  color: #000; /* Set icon color */
}

/* Main content section - Add margin to position it below the top */
.v-main {
  padding-right: 250px; /* Space for the navigation drawer */
  margin-top: 55px; /* Add 55px margin to push the content down */
}

/* Background Image Styling */
.home-page {
  /* background-image: url('@/assets/images/login_bg.jpg'); /* Path to your image in the assets folder */
  background-size: cover; /* Ensure the background image covers the whole area */
  background-position: center center; /* Center the image */
  height: 100vh; 
  width: 100vw;
  /* padding: 20px; Optional padding */
}

/* Custom font size for list items */
.v-list-item-title {
  font-size: 15px; /* Adjust font size to make it smaller */
  font-weight: normal; /* Optional: adjust font weight if needed */
}

.menu-list {
  /* display: flex; */
  flex-direction: column;
  justify-content: center; /* Vertically center the items */
  align-items: center; /* Horizontally center the items */
  height: 100vh; /* Full height of the viewport */
  width: 100%;
}

/* Align the icon and text in a row */
.v-list-item {
  display: flex;
  align-items: center; /* Ensure the icon and text are aligned */
}

/* Optionally add space between the icon and the text */
.v-list-item-icon {
  margin-right: 10px;
}

.item-font {
  font-weight: 1000;
}

.logout-font {
  color: rgb(188, 48, 48);
  font-weight: 1000;
}
</style>
