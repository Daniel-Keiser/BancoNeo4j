<template>
  <div class="container">
    <h2>Criar Novo Paciente</h2>
    <form @submit.prevent="submitAppointment">
      <div class="form-group">
        <label for="patientSelect">Selecione um Usuário:</label>
        <select id="patientSelect" v-model="selectedUserID" class="select-field">
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.username }}
          </option>
        </select>
        {{selectedUserID}}
      </div>

      <div class="form-group">
        <label for="entereço">Endereço</label>
        <textarea id="entereço" v-model="newPatient.address"></textarea>
      </div>
      <div class="form-group">
        <label for="telefone">Telefone</label>
        <textarea id="telefone" v-model="newPatient.phone_number"></textarea>
      </div>
      <div class="form-group">
        <label for="emergency">Contato de Emergência</label>
        <textarea id="emergency" v-model="newPatient.contact_emergency"></textarea>
      </div>
      <div class="form-group">
        <label for="idade">Idade</label>
        <input type="number" id="idade" v-model="newPatient.age" required>
      </div>
      <div class="form-group">
        <label for="h-medico">Histórico Médico</label>
        <textarea id="h-medico" v-model="newPatient.medical_history"></textarea>
      </div>

      <button type="submit">Criar Paciente</button>
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
      selectedUserID: null,
      newPatient: {
        medical_history: null,
        contact_emergency: null,
        address: null,
        phone_number: null,
        age: null,
      }
    };
  },
  methods: {
    async submitAppointment() {
      try {
        const newPatientData = {
          user_id: this.selectedUserID,
          medical_history: this.newPatient.medical_history,
          contact_emergency: this.newPatient.contact_emergency,
          address: this.newPatient.address,
          phone_number: this.newPatient.phone_number,
          age: this.newPatient.age
        };

        // Faça a solicitação POST para o endpoint de criação de agendamento
        const response = await axios.post('http://localhost:8000/patients', newPatientData);

        if (response.status === 200) {
          // O agendamento foi criado com sucesso, você pode redirecionar o usuário ou fazer outra ação
          this.$router.push('/pacientes'); // Redirecionar de volta à lista de agendamentos
        }
      } catch (error) {
        console.error('Erro ao criar paciente:', error);
      }
    },
    async fetchPatients() {
      try {
        const response = await fetch('http://localhost:8000/users', { method: 'GET' });
        if (response.ok) {
          const data = await response.json();
          this.users = data;
        } else {
          console.error('Erro ao buscar usuário.');
        }
      } catch (error) {
        console.error('Erro ao buscar usuário:', error);
      }
    },
  },
  mounted() {
    this.fetchPatients();
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

