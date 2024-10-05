<template>
  <h1 class="text-center mt-4 mb-4">Графики по обработанным вакансиям</h1>
  <div class="container mt-4">
    <div class="row mt-4">
      <div class="col-md-6 mb-4">
        <div class="form-group">
          <label for="yearSelector">Выберите год:</label>
          <select id="yearSelector" class="form-control" v-model="selectedYear" @change="updateChartData">
            <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
          </select>
        </div>
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Среднее количество дней закрытия вакансии</h5>
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
      <div class="col-md-6 mb-4">
        <div class="form-group">
          <label for="yearSelector">Выберите рекуртера:</label>
          <select id="yearSelector" class="form-control" v-model="itemChertRecruter" @change="updatePerformanceChart">
            <option v-for="recruter in chartRecruters" :key="recruter">{{ recruter }}</option>
          </select>
        </div>
        <div class="card">
          <div class="card-body">
            <h5>Время скрининга</h5>
            <canvas id="recruiterChart" ref="recruiterChart" v-if="recruitersData.length"></canvas>
            <p v-else>Нет данных для отображения</p>
          </div>
        </div>
      </div>
      <div class="col-md-6 mb-4">
        <div class="form-group">
          <label for="yearSelector">Выберите рекуртера:</label>
          <select id="yearSelector" class="form-control" v-model="itemQualityRecruter" @change="updateHireQualityChart">
            <option v-for="recruter in qualitiesRecruters" :key="recruter">{{ recruter }}</option>
          </select>
        </div>
        <div class="card">
          <div class="card-body">
            <h5>Качество найма по рекрутеру за период</h5>
            <canvas id="qualityChart" ref="qualityChart" v-if="hireQualityData.length"></canvas>
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
  BarController,    
  CategoryScale,   
  LinearScale,     
  LineElement,
  BarElement,   
  PointElement,    
  Title,           
  Tooltip,     
  TimeScale,     
  Legend            
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { apiUrl } from '@/api';

ChartJS.register(
  BarController,
  CategoryScale,
  LinearScale,
  LineElement,
  BarElement,
  PointElement,
  Title,
  Tooltip,
  TimeScale,
  Legend
);

export default {
  name: 'BarChart',
  components: {
    LineChart: Line,
  },
  data() {
    return {
      availableYears: [],
      selectedYear: null,
      chartData: { datasets: [] },
      chartTitle: '',
      chartOptions: {
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'month',
              tooltipFormat: 'MMM yyyy',
              displayFormats: { month: 'MMM' },
            },
            title: { display: true, text: 'Месяц' },
          },
          y: {
            title: { display: true, text: 'Количество вакансий' },
          },
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: (context) => {
                const date = new Date(context.parsed.x);
                const month = this.monthNames[date.getMonth()];
                const value = context.parsed.y;
                return `${month}: ${value} вакансий`;
              },
            },
          },
        },
      },
      jsonData: {},
      monthNames: [
        'Январь', 'Февраль', 'Март', 'Апрель',
        'Май', 'Июнь', 'Июль', 'Август',
        'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
      ],
      chartInstance: null,
      chartQualityInstance: null,
      itemChertRecruter: null,
      itemQualityRecruter: null,
      chartRecruters: [],
      qualitiesRecruters: [],
      formattedPerformanceData: [],
      formattedHireQualityData: [],
      recruitersData: [],
      hireQualityData: []
    };
  },
  mounted() {
    this.fetchVacancyData();
    this.fetchPerformanceChart();
    this.fetchHireQualityChart();
  },
  methods: {
    async fetchVacancyData() {
      try {
        const response = await fetch(`${apiUrl}/metrics/average-hire-time`);
        const data = await response.json();
        this.jsonData = data.data;
        this.availableYears = Object.keys(this.jsonData);
        this.selectedYear = this.availableYears[0];
        this.updateChartVacancyData();
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    },
    transformVacancyData(data) {
      return Object.entries(data).map(([month, { vacancies_count }]) => ({
        x: new Date(`${this.selectedYear}-${month}-01`),
        y: vacancies_count,
      }));
    },
    updateChartVacancyData() {
      const yearData = this.jsonData[this.selectedYear];
      if (!yearData) {
        console.log(`Нет данных для года ${this.selectedYear}`);
        return;
      }

      const transformedData = this.transformVacancyData(yearData);
      this.chartData = {
        datasets: [{
          label: `Количество вакансий за ${this.selectedYear} год`,
          data: transformedData,
          fill: false,
          borderColor: '#FF6384',
          tension: 0.1,
        }],
      };

      this.chartTitle = `Количество вакансий за ${this.selectedYear} год`;
    },
    async transformRecruterData() {
      this.formattedPerformanceData = {};
      for (let item of this.recruitersData) {
        if (!this.itemChertRecruter) {
          this.itemChertRecruter = item.recruiter_name;
        }
        if (this.chartRecruters.indexOf(item.recruiter_name) == -1) {
          this.chartRecruters.push(item.recruiter_name);
        }
        if (!this.formattedPerformanceData[item.recruiter_name]) {
          this.formattedPerformanceData[item.recruiter_name] = [
            {month: item.month, value: item.value}
          ];
        } else {
          this.formattedPerformanceData[item.recruiter_name].push({month: item.month, value: item.value});
        }
      }
    },
    async fetchPerformanceChart() { 
      try {
        const response = await fetch(`${apiUrl}/metrics/screen-time`);
        if (!response.ok) {
          throw new Error(`Ошибка сети: ${response.statusText}`);
        }
        this.recruitersData = await response.json();
        await this.transformRecruterData();
        await this.updatePerformanceChart();
      } catch (error) {
        console.error('Ошибка при загрузке данных для графика:', error);
      }
    },
    updatePerformanceChart() { 

      if (!Object.keys(this.formattedPerformanceData).length) {
        return;
      }
      const labels = this.formattedPerformanceData[this.itemChertRecruter].map(item => item.month);
      const values = this.formattedPerformanceData[this.itemChertRecruter].map(item => item.value);
      const ctx = this.$refs.recruiterChart.getContext('2d');

      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      this.chartInstance = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Производительность ' + this.itemChertRecruter,
            data: values,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          }],
        },
        options: {
          scales: {
            x: {
              type: 'category', // Set x-axis type to category
              title: {
                display: true,
                text: 'Время',
              },
            },
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Производительность',
              },
            },
          },
        },
      });
    },
    async fetchHireQualityChart() { 
      try {
        const response = await fetch(`${apiUrl}/metrics/hire-quality`);
        if (!response.ok) {
          throw new Error(`Ошибка сети: ${response.statusText}`);
        }
        this.hireQualityData = await response.json();
        await this.transformHireQualityData();
        await this.updateHireQualityChart();
      } catch (error) {
        console.error('Ошибка при загрузке данных для графика:', error);
      }
    },
    async transformHireQualityData() {
      this.formattedHireQualityData = {};
      for (let item of this.hireQualityData) {
        if (!this.itemQualityRecruter) {
          this.itemQualityRecruter = item.recruiter_name;
        }
        if (this.qualitiesRecruters.indexOf(item.recruiter_name) == -1) {
          this.qualitiesRecruters.push(item.recruiter_name);
        }
        if (!this.formattedHireQualityData[item.recruiter_name]) {
          this.formattedHireQualityData[item.recruiter_name] = [
            {month: item.month, value: item.value}
          ];
        } else {
          this.formattedHireQualityData[item.recruiter_name].push({month: item.month, value: item.value});
        }
      }
    },
    updateHireQualityChart() { 

      if (!Object.keys(this.formattedHireQualityData).length) {
        return;
      }
      const labels = this.formattedHireQualityData[this.itemQualityRecruter].map(item => item.month);
      const values = this.formattedHireQualityData[this.itemQualityRecruter].map(item => item.value);
      const ctx = this.$refs.qualityChart.getContext('2d');

      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      
      if (this.chartQualityInstance) {
        this.chartQualityInstance.destroy();
      }

      this.chartQualityInstance = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Производительность ' + this.itemQualityRecruter,
            data: values,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          }],
        },
        options: {
          scales: {
            x: {
              type: 'category', // Set x-axis type to category
              title: {
                display: true,
                text: 'Время',
              },
            },
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Производительность',
              },
            },
          },
        },
      });
    }
  }
}
</script>


<style scoped>
.card {
  margin-top: 20px;
  height: 380px
}
</style>
