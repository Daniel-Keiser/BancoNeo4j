<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">Agendify</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/agendamentos">Agendamentos</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/pacientes">Pacientes</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/medicos">Médicos</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/usuarios">Usuários</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/status">Status</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/especialidades">Especialidades</RouterLink>
        </li>
      </ul>
    </div>
  </nav>
</template>



