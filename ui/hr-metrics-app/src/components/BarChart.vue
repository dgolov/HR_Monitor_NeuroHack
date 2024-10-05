<template>
  <h1 class="text-center mt-4">Графики по обработанным вакансиям</h1>
  <div class="container mt-4">
    <div class="form-group">
      <label for="yearSelector">Выберите год:</label>
      <select id="yearSelector" class="form-control" v-model="selectedYear" @change="updateChartData">
        <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
      </select>
    </div>

    <div class="row mt-4">
      <div class="col-md-12 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ chartTitle }}</h5>
            <line-chart
              v-if="chartData.datasets.length > 0"
              :data="chartData"
              :colors="['#FF6384']"
              :options="chartOptions"
            />
            <p v-else>Нет данных для отображения</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  TimeScale,
  Filler
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { apiUrl } from '@/api';

// Регистрация всех необходимых компонентов и шкал
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, TimeScale, Filler);

export default {
  name: 'BarChart',
  components: {
    LineChart: Line,
  },
  data() {
    return {
      availableYears: [], // Доступные года
      selectedYear: null, // Выбранный год
      chartData: {
        datasets: [],
      },
      chartTitle: '', // Заголовок графика
      chartOptions: {
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'month',
              tooltipFormat: 'MMM yyyy',
              displayFormats: {
                month: 'MMM',
              },
            },
            title: {
              display: true,
              text: 'Месяц',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Количество вакансий',
            },
          },
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: (context) => {
                // Преобразуем x в объект Date
                const date = new Date(context.parsed.x);
                const month = this.monthNames[date.getMonth()]; // Получаем название месяца
                const value = context.parsed.y; // Получаем значение по оси Y
                return `${month}: ${value} вакансий`; // Формируем строку для тултипа
              },
            },
          },
        },
      },
      jsonData: {}, // Данные, полученные с API
      monthNames: [
        'Январь', 'Февраль', 'Март', 'Апрель',
        'Май', 'Июнь', 'Июль', 'Август',
        'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
      ], // Названия месяцев на русском
    };
  },
  mounted() {
    this.fetchData(); // Получаем данные с API при монтировании компонента
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch(`${apiUrl}/metrics/average-hire-time`);
        const data = await response.json();
        this.jsonData = data.data; // Предполагаем, что данные находятся внутри data
        this.availableYears = Object.keys(this.jsonData); // Получаем доступные года
        this.selectedYear = this.availableYears[0]; // Устанавливаем первый год как выбранный
        this.updateChartData(); // Инициализация данных графика
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    },
    transformData(data) {
      return Object.entries(data).map(([month, { vacancies_count }]) => ({
        x: new Date(`${this.selectedYear}-${month}-01`), // Форматируем дату для ISO
        y: vacancies_count,
      }));
    },
    updateChartData() {
      const yearData = this.jsonData[this.selectedYear];
      if (!yearData) {
        console.log(`Нет данных для года ${this.selectedYear}`);
        return; // Если нет данных, выходим из метода
      }

      const transformedData = this.transformData(yearData); // Преобразуем все данные года

      this.chartData = {
        datasets: [{
          label: `Количество вакансий за ${this.selectedYear} год`,
          data: transformedData,
          fill: false,
          borderColor: '#FF6384',
          tension: 0.1,
        }],
      };

      // Обновляем заголовок графика
      this.chartTitle = `Количество вакансий за ${this.selectedYear} год`;
    },
  },
};
</script>

<style scoped>
.card {
  margin-top: 20px; /* Установите отступ сверху для карточки */
}
</style>
