import { createApp } from 'vue'; // Используйте правильный импорт для Vue 3
import 'bootstrap/dist/css/bootstrap.min.css';
import App from './App.vue';
import router from "@/routes/index";
import DefaultLayout from "./layouts/DefaultLayout";

// Создайте приложение
const app = createApp(App);

// Глобальная регистрация компонента в Vue 3
app.component("default-layout", DefaultLayout); // Имя компонента должно быть в нижнем регистре с дефисом

// Подключаем роутер и монтируем приложение
app.use(router).mount('#app');
