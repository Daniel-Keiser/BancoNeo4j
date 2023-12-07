<template>
  <div class="container">
    <RouterLink class="create-button" to="/novo_status">Criar Status</RouterLink>

    <ul class="patient-list">

      <li v-for="statu in status" :key="statu.id" class="patient-item">
        <div class="info">
          <p class="patient">Status: {{ statu.name }}</p>
          <button @click="deleteStatus(statu.id)" class="delete-button">Excluir</button>
        </div>
      </li>
    </ul>

  </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router'

export default {
  name: 'Pacientes',
  data() {
    return {
      status: [],
    };
  },
  methods: {
    async deleteStatus(status) {
      try {
        const response = await fetch(`http://localhost:8000/appointment-statuses/${status}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          // Atualize a lista de agendamentos após a exclusão bem-sucedida
          this.fetchStatus();
        } else {
          console.error('Erro ao excluir usuário.');
        }
      } catch (error) {
        console.error('Erro ao excluir usuário:', error);
      }
    },
    async fetchStatus() {
      try {
        const response = await fetch('http://localhost:8000/appointment-statuses', { method: 'GET' });
        if (response.ok) {
          const data = await response.json();
          this.status = data;
        } else {
          console.error('Erro ao buscar status.');
        }
      } catch (error) {
        console.error('Erro ao buscar status:', error);
      }
    },
  },
  mounted() {
    this.fetchStatus();
  },
};
</script>

<style scoped>
/* Estilos para a lista de compromissos */
.patient-list {
  list-style-type: none;
  padding: 0;
}

.patient-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
  background-color: #f7f7f7;
}

/* Estilos para as informações dos compromissos */
.info {
  margin-left: 20px;
}

.patient, .doctor {
  font-weight: bold;
}

.specialty {
  font-style: italic;
}

.datetime, .status {
  color: #333;
}

.observations {
  margin-top: 5px;
}

.duration {
  font-weight: bold;
  margin-top: 5px;
}

.create-button{
  display: inline-block;
  font-weight: 400;
  text-align: center;
  margin-top: 1%;
  white-space: nowrap;
  vertical-align: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  border: 1px solid transparent;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  border-radius: 0.25rem;
  transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;
  color: #000;
  background-color: #ffffff;
  border-color: #001944;
}

.delete-button {
  color: #fff;
  background-color: #dc3545;
  border-color: #dc3545;
  display: inline-block;
  font-weight: 400;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  border: 1px solid transparent;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  border-radius: 0.25rem;
  transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;
}

.edit-button {
  margin-right: 1%;
  color: #fff;
  background-color: #0a4efa;
  border-color: #0a4efa;
  display: inline-block;
  font-weight: 400;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  border: 1px solid transparent;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  border-radius: 0.25rem;
  transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;
}

</style>
