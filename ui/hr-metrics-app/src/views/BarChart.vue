<template>
  <h1 class="text-center mt-4 mb-4">Метрики эффективности</h1>
  <hr/>
  <div class="container mt-4">
    <div class="row mt-4">
      <div class="col-md-6">
        <div v-if="itemRecruter" class="d-flex align-items-center recruiter-card p-3 shadow-sm">
          <div class="recruiter-info">
            <h5>{{ itemRecruter.name }}</h5>
            <p><strong>Телефон:</strong> {{ itemRecruter.phone }}</p>
            <p><strong>Email:</strong> {{ itemRecruter.email }}</p>
            <p><strong>Грейд:</strong> 5 / 5</p>
            <p><strong>Оценка эффективности:</strong> 4 / 5</p>
          </div>
          <div class="recruiter-photo ms-4">
            <img src="@/static/0471dab9-d6c5-4d64-a002-59de01a881db.webp" 
              alt="Фото рекрутера" 
              class="img-fluid rounded-circle" 
              style="width: 120px; height: 120px;" />
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="form-group mb-3">
          <label for="recruterSelector">Выберите рекрутера:</label>
          <select id="recruterSelector" class="form-control mt-1" v-model="itemRecruter" @change="updateData">
            <option v-for="recruter in recruters" :key="recruter" :value="recruter">{{ recruter.name }}</option>
          </select>
        </div>
        <div class="row mt-4 align-items-end">
          <div class="col-md-4">
            <div class="form-group">
              <label for="startDate">Start Date:</label>
              <Datepicker 
                v-model="startDate"
                :format="dateFormat"
                input-class="form-control"
              />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label for="endDate">End Date:</label>
              <Datepicker 
                v-model="endDate"
                :format="dateFormat"
                input-class="form-control"
              />
            </div>
          </div>
          <div class="col-md-4">
            <button class="btn btn-secondary mt-4" style="height: 30px;">Применить</button>
          </div>
        </div>

      </div>
      <div class="col-md-6 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Среднее количство дней на закрытие вакансий</h5>
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
        <div class="card">
          <div class="card-body">
            <h5>Время скрининга</h5>
            <canvas id="recruiterChart" ref="recruiterChart" v-if="recruitersData.length"></canvas>
            <p v-else>Нет данных для отображения</p>
          </div>
        </div>
      </div>
      <div class="col-md-6 mb-4">
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
import Datepicker from 'vue3-datepicker';
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
    LineChart: Line, Datepicker
  },
  data() {
    return {
      recruters: [],
      itemRecruter: null,
      availableYears: [],
      selectedYear: null,
      chartData: { datasets: [] },
      chartTitle: '',
      recruterID: '',
      chartOptions: {
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'month',
              tooltipFormat: 'MMM yyyy',
              displayFormats: { month: 'MMM' },
            },
            title: { display: true, text: '' },
          },
          y: {
            title: { display: true, text: 'Количество' },
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
      colorPalette: [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#4B77BE','#F5D76E', '#AAB7B8', '#F1948A' 
      ],
      currentColorIndex: 0,
      chartInstance: null,
      chartQualityInstance: null,
      itemChertRecruter: null,
      itemQualityRecruter: null,
      chartRecruters: [],
      qualitiesRecruters: [],
      formattedPerformanceData: [],
      formattedHireQualityData: [],
      recruitersData: [],
      hireQualityData: [],
      startDate: null,
      endDate: null,
      dateFormat: 'yyyy-MM-dd',
    };
  },
  created() {
    this.fetchRecruterst();
    this.fetchVacancyData();
    this.fetchPerformanceChart();
    this.fetchHireQualityChart();
  },
  methods: {
    updateData() {
      this.currentColorIndex = 0;
      this.fetchVacancyData();
      this.updateHireQualityChart();
      this.updatePerformanceChart();
    },
    async fetchRecruterst() { 
      try {
        const response = await fetch(`${apiUrl}/users/?role=recruiter`);
        if (!response.ok) {
          throw new Error(`Ошибка сети: ${response.statusText}`);
        }
        this.recruters = await response.json();
        this.itemRecruter = this.recruters[0]
      } catch (error) {
        console.error('Ошибка при загрузке рекрутеров:', error);
      }
    },
    async fetchVacancyData() {
      try {
        let url = `${apiUrl}/metrics/average-hire-time`;
        if (this.itemRecruter) {
          url += `?recruiter_id=${this.itemRecruter.id}`;
        }
        const response = await fetch(url);
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
    getNextColor() {
      const color = this.colorPalette[this.currentColorIndex];
      this.currentColorIndex++;
      if (this.currentColorIndex >= this.colorPalette.length) {
        this.currentColorIndex = this.colorPalette.length - 1;
      }
      console.log(color)
      return color;
    },
    updateChartVacancyData() {
      this.chartData = {
        datasets: [],
      };

      for (let year of this.availableYears) {
        const yearData = this.jsonData[year];
        if (!yearData) {
          console.log(`Нет данных для года ${this.selectedYear}`);
          continue;
        }
        const transformedData = this.transformVacancyData(yearData);
        this.chartData.datasets.push({
          label: `${year} год`,
          data: transformedData,
          fill: false,
          borderColor: this.getNextColor(),
          tension: 0.1,
        })
      }

      this.chartTitle = `Среднее количство за ${this.selectedYear} год`;
    },
    async transformRecruterData() {
      this.formattedPerformanceData = {};
      for (let item of this.recruitersData) {
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
      if (!Object.keys(this.formattedPerformanceData).length || this.formattedPerformanceData[this.itemRecruter.name] == undefined) {
        return;
      }
      const labels = this.formattedPerformanceData[this.itemRecruter.name].map(item => item.month);
      const values = this.formattedPerformanceData[this.itemRecruter.name].map(item => item.value);
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
            label: 'Производительность ' + this.itemRecruter.name,
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
      if (!Object.keys(this.formattedHireQualityData).length || this.formattedHireQualityData[this.itemRecruter.name] == undefined) {
        return;
      }
      const labels = this.formattedHireQualityData[this.itemRecruter.name].map(item => item.month);
      const values = this.formattedHireQualityData[this.itemRecruter.name].map(item => item.value);
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
            label: 'Качество найма ' + this.itemRecruter.name,
            data: values,
            backgroundColor: 'rgba(255, 159, 64, 0.2)', 
            borderColor: 'rgba(255, 159, 64, 1)',  
            borderWidth: 1,
          }],
        },
        options: {
          scales: {
            x: {
              type: 'category',
              title: {
                display: true,
                text: 'Время',
              },
            },
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Качество',
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
.recruiter-card {
  background-color: #f9f9f9;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recruiter-info h5 {
  font-size: 1.25rem;
  font-weight: bold;
}

.recruiter-info p {
  font-size: 0.9rem;
  margin: 0;
}

.recruiter-photo img {
  border-radius: 50%;
  border: 2px solid #ccc;
}

.form-control {
  border-radius: 5px;
}

.card {
  margin-top: 20px;
  height: 380px;
  border-radius: 10px;
}

.card-body {
  padding: 20px;
}

h5 {
  font-weight: bold;
}
</style>
