<template>
  <div id="app">
    <AppNavbar />
    <BarChart />
    <KanbanBoard />
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue';
import BarChart from './views/BarChart.vue';

export default {
  name: 'App',
  components: {
    BarChart,
    AppNavbar
  }
};
</script>

<style>
/* Основные стили */
#app {
  text-align: center;
}
</style>

