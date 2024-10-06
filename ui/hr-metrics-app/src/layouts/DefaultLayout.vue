<template>
    <div id="app">
      <AppNavbar />
      <router-view/>
    </div>
  </template>
  
  <script>
  import AppNavbar from '@/components/AppNavbar.vue';
  
  export default {
    name: "DefaultLayout",
    components: {
        AppNavbar,
    },
  }
  </script>
  
  <style>
  </style>
  

