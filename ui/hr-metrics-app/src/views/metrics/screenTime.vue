<template>
    <div class="container mt-4">
        <h2 class="text-center mb-4">Время скрининга</h2>
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Рекрутер</th>
            <th scope="col">Дата</th>
            <th scope="col">Значение</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in data" :key="item.id">
            <td>{{ item.recruiter_name }}</td>
            <td>{{ item.month }}</td>
            <td>{{ item.value }}</td>
          </tr>
        </tbody>
      </table>
  
      <!-- <nav aria-label="Page navigation" class="mt-4">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <a class="page-link" @click="changePage(currentPage - 1)" href="#">Назад</a>
          </li>
          <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
            <a class="page-link" @click="changePage(page)" href="#">{{ page }}</a>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <a class="page-link" @click="changePage(currentPage + 1)" href="#">Вперед</a>
          </li>
        </ul>
      </nav> -->
    </div>
  </template>
  
  <script>
  import { apiUrl } from '@/api';

  export default {
    data() {
      return {
        currentPage: 1,
        data: [],
        offset: 50
      };
    },
    computed: {
      totalPages() {
        return 10;
      },
      paginatedCandidates() {
        const start = (this.currentPage - 1) * this.offset;
        return this.candidates.slice(start, start + this.offset);
      },
    },
    created() {
        this.fetchData();
    },
    methods: {
        async fetchData() { 
            try {
                const response = await fetch(`${apiUrl}/metrics/screen-time`);
                if (!response.ok) {
                throw new Error(`Ошибка сети: ${response.statusText}`);
                }
                this.data = await response.json();
            } catch (error) {
                console.error('Ошибка при загрузке рекрутеров:', error);
            }
        },
        mapStatus(statusValue) {
            for (let baseStatus of this.statuses) {
                if (statusValue == baseStatus.value) {
                    return baseStatus.name;
                }
            }
            return "Не определен";
        },
        changePage(page) {
            if (page < 1 || page > this.totalPages) return;
            this.currentPage = page;
            this.updateURL();
            this.fetchCandidates();
        },
        updateURL() {
            const url = new URL(window.location);
            url.searchParams.set('page', this.currentPage);
            window.history.pushState({}, '', url);
        },
    },
    mounted() {
      const urlParams = new URLSearchParams(window.location.search);
      const page = parseInt(urlParams.get('page'));
      if (page) {
        this.currentPage = page;
      }
    },
  };
  </script>
  
  <style scoped>
  .table th {
    background-color: #f8f9fa;
  }
  .pagination .page-link {
    color: #6c757d;
  }
  .pagination .page-item.disabled .page-link {
    color: #6c757d; 
  }
  .pagination .active .page-link {
  background-color: #6c757d; 
  color: #fff;
}
  </style>
  