<template>
  <div class="container">
    <h2>Criar Novo Médico</h2>
    <form @submit.prevent="submitDoctor">
      <div class="form-group">
        <label for="patientSelect">Selecione um Usuário:</label>
        <select id="patientSelect" v-model="selectedUserId" class="select-field">
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.username }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="doctorSelect">Selecione uma Especialidade:</label>
        <select id="doctorSelect" v-model="selectedSpecialtyId" class="select-field">
          <option v-for="specialtie in specialties" :key="specialtie.id" :value="specialtie.id">
            {{ specialtie.name }}
          </option>
        </select>
      </div>
      <button type="submit">Criar Médico</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'NewAppointment',
  data() {
    return {
      users: [],
      specialties: [],
      selectedUserId: null,
      selectedSpecialtyId: null,
      newDoctor: {}
    };
  },
  methods: {
    async submitDoctor() {
      try {
        const newDoctor = {
          user_id: this.selectedUserId,
          specialization_id: this.selectedSpecialtyId,
        };

        // Faça a solicitação POST para o endpoint de criação de agendamento
        const response = await axios.post('http://localhost:8000/doctors', newDoctor);

        if (response.status === 201) {
          // O agendamento foi criado com sucesso, você pode redirecionar o usuário ou fazer outra ação
          this.$router.push('/medicos'); // Redirecionar de volta à lista de agendamentos
        }
      } catch (error) {
        console.error('Erro ao criar médico:', error);
      }
    },
    async fetchUsers() {
      try {
        const response = await fetch('http://localhost:8000/users', { method: 'GET' });
        if (response.ok) {
          const data = await response.json();
          this.users = data;
        } else {
          console.error('Erro ao buscar usuários.');
        }
      } catch (error) {
        console.error('Erro ao buscar usuários:', error);
      }
    },
    async fetchSpecialty() {
      try {
        const response = await fetch('http://localhost:8000/specialties', { method: 'GET' });
        if (response.ok) {
          const data = await response.json();
          this.specialties = data;
        } else {
          console.error('Erro ao buscar especialidades.');
        }
      } catch (error) {
        console.error('Erro ao buscar especialidades:', error);
      }
    },
  },
  mounted() {
    this.fetchUsers();
    this.fetchSpecialty();
  },
  computed: {
  }
};
</script>

<style scoped>
/* Estilos para o formulário de criação de agendamento */
.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
}

input[type="text"],
input[type="number"],
textarea,
input[type="datetime-local"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="submit"] {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}
/* Estilos para o campo de seleção de paciente */
.select-field {
  padding: 10px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  font-size: 16px;
  color: #333;
}

/* Estilos para o botão de seleção */
button {
  margin-top: 10px;
  margin-bottom: 10px;
  padding: 10px 20px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>

