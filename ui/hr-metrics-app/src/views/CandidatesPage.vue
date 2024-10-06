<template>
    <div class="container mt-4">
      <h2 class="text-center mb-4">Список кандидатов</h2>
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
          <tr v-for="candidate in paginatedCandidates" :key="candidate.uuid">
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
            <td>{{ candidate.status }}</td>
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
  export default {
    data() {
      return {
        currentPage: 1,
        candidates: [
          {
            id: 1,
            uuid: "f6ee4ec0-8f2f-4fa4-8aa8-54ed0b7e5900",
            name: "Julia Lowery",
            is_referral: true,
            other_info: {
              hobbies: ["woman", "pull", "commercial"],
              experience: "Lecturer, higher education",
            },
            resume_link: "https://phillips.com/",
            status: "hired",
            vacancy_id: 7,
          },
          {
            id: 2,
            uuid: "d05fbec0-d6e7-45a6-acef-7b1b483a334c",
            name: "Christopher Parker",
            is_referral: true,
            other_info: {
              hobbies: ["sort", "front", "low"],
              experience: "Waste management officer",
            },
            resume_link: "https://www.patel.com/",
            status: "interviewed",
            vacancy_id: 9,
          },
          // Добавьте больше кандидатов для тестирования пагинации
          {
            id: 3,
            uuid: "d3fbedbc-ecf2-44d8-8ed2-6d99bde00f3f",
            name: "Alice Johnson",
            is_referral: false,
            other_info: {
              hobbies: ["reading", "traveling", "music"],
              experience: "Software Engineer",
            },
            resume_link: "https://example.com/",
            status: "hired",
            vacancy_id: 10,
          },
          {
            id: 4,
            uuid: "4c3d69c1-0ecf-43da-84da-3d6815c8d215",
            name: "David Smith",
            is_referral: false,
            other_info: {
              hobbies: ["gaming", "cooking"],
              experience: "Data Analyst",
            },
            resume_link: "https://example.com/",
            status: "pending",
            vacancy_id: 11,
          },
          // ... добавьте больше кандидатов для тестирования пагинации
        ],
      };
    },
    computed: {
      totalPages() {
        return Math.ceil(this.candidates.length / 2); // Предположим, что мы показываем 2 кандидата на странице
      },
      paginatedCandidates() {
        const start = (this.currentPage - 1) * 2;
        return this.candidates.slice(start, start + 2);
      },
    },
    methods: {
      changePage(page) {
        if (page < 1 || page > this.totalPages) return;
        this.currentPage = page;
        this.updateURL();
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
    color: #6c757d; /* Цвет текста */
  }
  .pagination .page-item.disabled .page-link {
    color: #6c757d; /* Цвет для отключенных ссылок */
  }
  .pagination .active .page-link {
  background-color: #6c757d; /* Цвет фона активной страницы */
  color: #fff; /* Цвет текста активной страницы */
}
  </style>
  