import { createApp } from 'vue'
import 'bootstrap/dist/css/bootstrap.min.css';
import App from './App.vue'
import router from "@/routes/index";


createApp(App)
  .use(router) // Подключите роутер к приложению
  .mount('#app');

