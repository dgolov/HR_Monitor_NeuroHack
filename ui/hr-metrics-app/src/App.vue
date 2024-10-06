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
#app {
  text-align: center;
}
a {
  color: brown;
}
</style>

