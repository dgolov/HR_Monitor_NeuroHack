import { createApp } from 'vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import App from './App.vue';
import router from "@/routes/index";
import DefaultLayout from "@/layouts/DefaultLayout";


const app = createApp(App);

app.component("default-layout", DefaultLayout);
app.use(router).mount('#app');
