<template>
  <div id="app">
    <component :is="layout"></component>
  </div>
</template>

<script>

export default {
  name: 'App',

  computed: {
    layout(){
      return this.$route.meta.layout || "default-layout"
    }
  }

};
</script>

<style>
/* Основные стили */
#app {
  text-align: center;
}
</style>

