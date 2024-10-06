<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-0"> <!-- Убираем отступ снизу -->
    <div class="container-fluid"> <!-- Изменяем на container-fluid для полной ширины -->
      <a class="navbar-brand" href="/">HR Монитор</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/"><i class="fas fa-home me-1"></i> Главная</a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="metricsDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="fas fa-chart-line me-1"></i> Метрики
            </a>
            <ul class="dropdown-menu" aria-labelledby="metricsDropdown">
              <li>
                <a class="dropdown-item" href="/metrics/average-hire-time">
                  <i class="fas fa-chart-bar me-1"></i> Среднее количество дней на закрытие вакансий
                </a>
              </li>
              <li>
                <a class="dropdown-item" href="/metrics/screen-time">
                  <i class="fas fa-chart-bar me-1"></i> Время скрининга
                </a>
              </li>
              <li>
                <a class="dropdown-item" href="/metrics/hire-quality">
                  <i class="fas fa-chart-bar me-1"></i> Качество найма за период
                </a>
              </li>
            </ul>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/candidates"><i class="fas fa-user-friends me-1"></i> Кандидаты</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/vacancies"><i class="fas fa-briefcase me-1"></i> Вакансии</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/interviews"><i class="fas fa-comments me-1"></i> Собеседования</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#"><i class="fas fa-tasks me-1"></i> Задачи</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/cabinet"><i class="fas fa-user-circle me-1"></i> Личный кабинет</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar',
};
</script>

<style scoped>
.navbar {
  margin: 0;
  padding: 0;
}
</style>
