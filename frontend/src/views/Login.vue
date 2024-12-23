<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-box">
        <h2>{{ isRegisterPage ? 'Register' : 'Login to continue' }}</h2>

        <!-- Login or Register Form -->
        <form @submit.prevent="handleSubmit" novalidate>

          <div class="input-group" v-if="!isRegisterPage">
            <label for="loginInput">{{ isEmailLogin ? 'Email' : 'Username' }}</label>
            <input
              type="text"
              v-model="loginInput"
              :placeholder="isEmailLogin ? 'Enter your email' : 'Enter your username'"
              required
            />
            <span v-if="errors.username" class="error">{{ errors.username }}</span>
          </div>

          <!-- Additional fields for registration page -->
          <div class="input-group" v-if="isRegisterPage">
            <label for="username">Username</label>
            <input
              type="text"
              v-model="username"
              placeholder="Choose a username"
              required
            />
            <span v-if="errors.username" class="error">{{ errors.username }}</span>
          </div>

          <div class="input-group" v-if="isRegisterPage">
            <label for="email">Email</label>
            <input
              type="email"
              v-model="email"
              placeholder="Enter your email"
              required
            />
            <span v-if="errors.email" class="error">{{ errors.email }}</span>
          </div>

          <!-- Password Field -->
          <div class="input-group">
            <label for="password">Password</label>
            <input
              type="password"
              v-model="password"
              placeholder="Enter your password"
              required
            />
            <span v-if="errors.password" class="error">{{ errors.password }}</span>
          </div>

          <div class="input-group" v-if="isRegisterPage">
            <label for="confirmPassword">Confirm Password</label>
            <input
              type="password"
              v-model="confirmPassword"
              placeholder="Confirm your password"
              required
            />
            <span v-if="errors.confirmPassword" class="error">{{ errors.confirmPassword }}</span>
          </div>

          <button type="submit">{{ isRegisterPage ? 'Register' : 'Login' }}</button>
        </form>

        <!-- Button container for side-by-side links -->
        <div class="button-container">

          <!-- Switch to email/username login link -->
          <span v-if="!isRegisterPage" class="link" @click="toggleLoginMethod">
            Switch to {{ isEmailLogin ? 'Username' : 'Email' }} Login
          </span>

          <!-- Register link or back to login -->
          <span class="link" @click="togglePage">
            {{ isRegisterPage ? 'Back to Login' : 'Register' }}
          </span>

        </div>
      </div>
    </div>

    <!-- register success notification -->
    <transition name="fade" @before-enter="beforeEnter" @after-leave="afterLeave">
      <div v-if="successMessage" class="notification success">
        {{ successMessage }}
      </div>
    </transition>

    <!-- login failure notification -->
    <transition name="fade" @before-enter="beforeEnter" @after-leave="afterLeave">
      <div v-if="failureMessage" class="notification failure">
        {{ failureMessage }}
      </div>
    </transition>

  </div>
</template>

<script>
import { getapi, postapi } from "../utils/http.js";

export default {
  data() {
    return {
      isEmailLogin: false, // Default to username login
      isRegisterPage: false, // Control whether we're on the register page
      loginInput: '',
      password: '',
      username: '',
      email: '',
      confirmPassword: '',
      errors: {
        username: '',
        email: '',
        confirmPassword: ''
      },
      successMessage: '',
      failureMessage: '',
    };
  },

  methods: {

    handleSubmit() {
      if (this.isRegisterPage) {
        this.handleRegister();
      } else {
        this.handleLogin();
      }
    },
    
    handleLogin() {
      // Perform login action
      if (this.isEmailLogin) {
        console.log('Logging in with Email:', this.loginInput);
      } else {
        console.log('Logging in with Username:', this.loginInput);
      }
      // Handle login logic
      
      // assert not empty
      this.errors = {
        username: '',
        password: '',
      };

      let isValid = true;

      if (this.loginInput.length <= 0 && this.isEmailLogin == false) {
        console.log('username empty')
        this.errors.username = 'Username is required';
        isValid = false;
      }

      if (this.loginInput.length <= 0 && this.isEmailLogin) {
        console.log('email empty')
        this.errors.username = 'Email is required';
        isValid = false;
      }

      if (this.password.length == 0) {
        this.errors.password = 'Password is required';
        isValid = false;
      }

      if (isValid) {
        // check if correct
        if (this.isEmailLogin) {
          this.validateLoginEmail(this.loginInput, this.password)
        } else {
          this.validateLoginUsername(this.loginInput, this.password)
        }
      }
    },

    async validateLoginEmail(email, password) {
      const data = { email, password }

      try {
        const response = await postapi('/api/user/login_email', data);

        console.log(response)

        if (!response.data.proceed) {
          // wrong combination
          this.failureMessage = 'Wrong email and/or password';

          setTimeout(() => {
            this.failureMessage = '';
          }, 3000);
        } else {
          // correct, logged in

          localStorage.setItem('is_login', true);
          this.$router.push('/');
          console.log('logged in!');
        }
      
      } catch (error) {

        console.log('error:', error);
      
      }
    },
    
    async validateLoginUsername(username, password) {
      const data = { username, password };

      try {
        const response = await postapi('api/user/login_username', data);

        console.log(response);

        if (!response.data.proceed) {
          this.failureMessage = 'Wrong username and/or password';
        
          setTimeout(() => {
            this.failureMessage = '';
          }, 3000);

        } else {
          localStorage.setItem('is_login', true);
          this.$router.push('/');
          console.log('logged in!');

        }
      } catch (error) {
        console.log('error:', error);
      }
    },

    async handleRegister() {
      // Reset errors
      this.errors = {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      };

      // Validate registration fields
      let isValid = true;

      // Validate username
      if (!this.username) {
        this.errors.username = 'Username is required';
        isValid = false;
      } else if (this.username.length <= 6) {
        this.errors.username = 'Username must be more than 6 characters';
        isValid = false;
      }

      // Validate email
      if (!this.email) {
        this.errors.email = 'Email is required';
        isValid = false;
      } else if (!this.isValidEmail(this.email)) {
        this.errors.email = 'Invalid email address';
        isValid = false;
      }

      // Validate password match
      if (this.password !== this.confirmPassword) {
        this.errors.confirmPassword = 'Passwords do not match';
        isValid = false;
      } 
      
      if (this.password.length <= 6) {
        this.errors.password = 'Password must be more than 6 characters';
        isValid = false;
      }

      // If everything is valid, submit the registration data
      if (isValid) {
        console.log('Registering with:', { username: this.username, email: this.email, password: this.password });

        const resp = await this.validateRegister(this.username, this.email, this.password);
        if (resp === 0) {
          isValid = true;
          this.isRegisterPage = false;

          this.successMessage = 'Registration successful!';

          // Hide the message after 3 seconds
          setTimeout(() => {
            this.successMessage = '';  // Hide the success message after 3 seconds
          }, 3000);

          console.log('register successful');
        } else if (resp === 1) {
          isValid = false;
          this.errors.username = 'Username already existed';
        } else if (resp === 2) {
          isValid = false;
          this.errors.email = 'Email already registered';
        }
      }
    },

    async validateRegister(username, email, password) {
      const data = { username, email, password };
      
      try {
        const response = await postapi('/api/user/register', data);

        console.log(response)
        // console.log(response.data.username, response.data.email);

        if (!response.data.username) {
          // username not unique
          return 1;
        }

        if (!response.data.email) {
          // email not unique
          return 2;
        }

        return 0; // everything looks good
      } catch (error) {
        this.result = '';
        console.log('error:', error);
        return -1; // return an error code in case the API request fails
      }
    },

    isValidEmail(email) {
      const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      return emailPattern.test(email);
    },

    togglePage() {
      this.isRegisterPage = !this.isRegisterPage; // Toggle between login and register pages
      this.resetForm();
    },

    resetForm() {
      // Reset form data when switching pages
      this.username = '';
      this.email = '';
      this.password = '';
      this.confirmPassword = '';
      this.loginInput = '';
      this.errors = {
        username: '',
        email: '',
        confirmPassword: ''
      };
    },

    toggleLoginMethod() {
      this.isEmailLogin = !this.isEmailLogin; // Toggle between email and username login
      this.loginInput = ''; // Clear input when switching methods
      this.errors = {
        username: '',
        email: '',
        password: '',
      };
    }
  }
};
</script>

<style scoped>
.login-page {
  margin-top: 55px;
  background-image: url('@/assets/images/login_bg.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.login-box {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
}

input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4c8cd0;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #2374d6;
}

.button-container {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 10px;
}

.link {
  font-size: 13px;
  color: #007bff;
  cursor: pointer;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
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
  border-radius: 8px;
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
