<template>
    <div class="container mt-4">
        <h2 class="text-center mb-4">Качество найма по рекрутеру за период</h2>
        <div class="d-flex justify-content-end mb-3">
            <button class="btn btn-secondary" @click="generateReport('hire-quality')">Сформировать отчет</button>
        </div>
        <div class="form-group mb-3" v-if="recruters.length">
            <label>Выберите рекрутера:</label>
            <div class="checkbox-group d-flex flex-wrap">
                <div v-for="recruter in recruters" :key="recruter.id" class="me-3">
                    <input type="checkbox" :value="recruter" v-model="selectedRecruters" @change="updateData"
                        id="recruter_{{ recruter.id }}" />
                    <label :for="'recruter_' + recruter.id">{{ recruter.name }}</label>
                </div>
            </div>
        </div>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">Рекрутер</th>
                    <th scope="col">Дата</th>
                    <th scope="col">Значение</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in filterredData" :key="item.id">
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
import { recrutersMixin } from "@/mixins/recrutersMixin";
import { orderMixin } from "@/mixins/orderMixin";

export default {
    data() {
        return {
            currentPage: 1,
            data: [],
            filterredData: [],
            selectedRecruters: [], // Хранит выбранных рекрутеров
            offset: 50,
        };
    },
    mixins: [recrutersMixin, orderMixin],
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
        this.fetchRecruterst();
        this.fetchData();
    },
    methods: {
        updateData() {
            if (this.selectedRecruters.length === 0) {
                this.filterredData = this.data;
            } else {
                this.filterredData = this.data.filter(item =>
                    this.selectedRecruters.some(recruter => recruter.name === item.recruiter_name)
                );
            }
        },
        async fetchData() {
            try {
                const response = await fetch(`${apiUrl}/metrics/hire-quality`);
                if (!response.ok) {
                    throw new Error(`Ошибка сети: ${response.statusText}`);
                }
                this.data = await response.json();
                this.filterredData = this.data;
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


.checkbox-group {
    display: flex;
    flex-wrap: wrap;
}

.checkbox-group div {
    display: flex;
    align-items: center;
}

.checkbox-group input[type="checkbox"] {
    margin-right: 10px;
}

.checkbox-group label {
    margin-left: 5px;
}
</style>