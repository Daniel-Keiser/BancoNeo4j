<template>
  <div class="container">
    <h2>Criar Novo Usuário</h2>
    <form @submit.prevent="submitUser">
      <div class="form-group">
        <label for="entereço">Username</label>
        <textarea id="entereço" v-model="newUser.username"></textarea>
      </div>
      <div class="form-group">
        <label for="telefone">Password</label>
        <input class="form-input" type="password" id="telefone" v-model="newUser.password">
      </div>
      <div class="form-group">
        <label for="emergency">Nome</label>
        <textarea id="emergency" v-model="newUser.first_name"></textarea>
      </div>
      <div class="form-group">
        <label for="idade">Sobrenome</label>
        <textarea type="number" id="idade" v-model="newUser.last_name"></textarea>
      </div>
      <div class="form-group">
        <label for="h-medico">Gênero</label>
        <textarea id="h-medico" v-model="newUser.gender"></textarea>
      </div>

      <button type="submit">Criar Usuário</button>
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
      newUser: {
        username: null,
        first_name: null,
        last_name: null,
        password: null,
        gender: null,
      }
    };
  },
  methods: {
    async submitUser() {
      try {
        const newUserData = {
          username: this.newUser.username,
          first_name: this.newUser.first_name,
          last_name: this.newUser.last_name,
          password: this.newUser.password,
          gender: this.newUser.gender,
        };

        // Faça a solicitação POST para o endpoint de criação de agendamento
        const response = await axios.post('http://localhost:8000/users', newUserData);

        if (response.status === 200) {
          // O agendamento foi criado com sucesso, você pode redirecionar o usuário ou fazer outra ação
          this.$router.push('/usuarios'); // Redirecionar de volta à lista de agendamentos
        }
      } catch (error) {
        console.error('Erro ao criar usuário:', error);
      }
    },
  },
  mounted() {
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

.form-input {
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

