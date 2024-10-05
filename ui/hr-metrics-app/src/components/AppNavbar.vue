<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-0"> <!-- Убираем отступ снизу -->
    <div class="container-fluid"> <!-- Изменяем на container-fluid для полной ширины -->
      <a class="navbar-brand" href="#">HR Монитор</a>
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
            <a class="nav-link active" aria-current="page" href="#"><i class="fas fa-home me-1"></i> Главная</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#"><i class="fas fa-user-friends me-1"></i> Кандидаты</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#"><i class="fas fa-briefcase me-1"></i> Вакансии</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#"><i class="fas fa-comments me-1"></i> Собеседования</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#"><i class="fas fa-user-circle me-1"></i> Личный кабинет</a>
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
/* Убираем отступы у навбара */
.navbar {
  margin: 0; /* Убираем отступы вокруг навбара */
  padding: 0; /* Убираем внутренние отступы */
}
</style>
