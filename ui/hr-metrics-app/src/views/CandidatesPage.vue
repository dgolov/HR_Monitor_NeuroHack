<template>
    <div class="container mt-4">
        <h2 class="text-center mb-4">Список кандидатов</h2>
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="form-group mb-3">
                    <label for="statusSelector">Выберите статус:</label>
                    <select 
                        id="statusSelector" 
                        class="form-control" 
                        v-model="currentStatus" 
                        @change="fetchCandidates"
                    >
                    <option key="" value="">Все</option>
                    <option v-for="status in statuses" :key="status.value" :value="status.value">
                        {{ status.name }}
                    </option>
                    </select>
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-group">
                    <div class="row d-flex align-items-center"> 
                        <div class="col-md-8">
                            <label>Фильтр по id вакансии:</label>
                            <input type="text" class="form-control" v-model="vacancyId" v-on:keyup.enter="fetchCandidates">
                        </div>
                        <div class="col-md-3 mt-4">
                            <button type="button" class="btn btn-secondary w-100" @click="fetchCandidates">Фильтр</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">ФИО</th>
            <th scope="col">Опыт</th>
            <th scope="col">Ссылка на резюме</th>
            <th scope="col">Хобби</th>
            <th scope="col">Статус</th>
            <th scope="col">Реферальная программа</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="candidate in candidates" :key="candidate.uuid">
            <td>{{ candidate.name }}</td>
            <td>{{ candidate.other_info.experience }}</td>
            <td>
              <a :href="candidate.resume_link" target="_blank" rel="noopener noreferrer">Резюме</a>
            </td>
            <td>
              <div>
                <span
                  v-for="hobby in candidate.other_info.hobbies"
                  :key="hobby"
                  class="badge bg-secondary me-1"
                >
                  {{ hobby }}
                </span>
              </div>
            </td>
            <td>{{ mapStatus(candidate.status) }}</td>
            <td>
              <span class="badge" :class="{'bg-success': candidate.is_referral, 'bg-secondary': !candidate.is_referral}">
                {{ candidate.is_referral ? 'Да' : 'Нет' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Пагинация -->
      <nav aria-label="Page navigation" class="mt-4">
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
      </nav>
    </div>
  </template>
  
  <script>
  import { apiUrl } from '@/api';

  export default {
    data() {
      return {
        currentPage: 1,
        currentStatus: "",
        vacancyId: "",
        candidates: [],
        offset: 50,
        statuses: [
            {value: "applied", name: "Принят"},
            {value: "interviewed", name: "Приглашен на собеседование"},
            {value: "hired", name: "Принят на работу"},
            {value: "rejected", name: "Отклонен"}
        ]
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
        this.fetchCandidates();
    },
    methods: {
        async fetchCandidates() { 
            try {
                const response = await fetch(`${apiUrl}/candidates/?status=${this.currentStatus}&vacancy_id=${this.vacancyId}&page=${this.currentPage}&offset=${this.offset}`);
                if (!response.ok) {
                throw new Error(`Ошибка сети: ${response.statusText}`);
                }
                this.candidates = await response.json();
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
  