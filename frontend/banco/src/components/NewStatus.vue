<template>
  <div class="container">
    <h2>Criar Novo Status</h2>
    <form @submit.prevent="submitStatus">
      <div class="form-group">
        <label for="observations">Nome</label>
        <textarea id="observations" v-model="name"></textarea>
      </div>
      <button type="submit">Criar Status</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'NewStatus',
  data() {
    return {
      name: null
    };
  },
  methods: {
    async submitStatus() {
      try {
        const params = new URLSearchParams();
        params.append('status_name', this.name);

        // Faça a solicitação POST para o endpoint de criação de status com os parâmetros de consulta
        const response = await axios.post('http://localhost:8000/appointment-statuses?' + params.toString());

        if (response.status === 200) {
          // O status foi criado com sucesso, você pode redirecionar o usuário ou fazer outra ação
          this.$router.push('/status'); // Redirecionar de volta à lista de status
        }
      } catch (error) {
        console.error('Erro ao criar status:', error);
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

