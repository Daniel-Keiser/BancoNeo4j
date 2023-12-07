<template>
  <div class="container">
    <RouterLink class="create-button" to="/novo_usuario">Criar Usuário</RouterLink>

    <ul class="patient-list">
      <li v-for="user in users" :key="user.id" class="patient-item">
        <div class="info">
          <p class="patient">Usuário: {{ user.username }}</p>
          <p class="">Nome: {{ user.first_name }} {{ user.last_name }}</p>
          <p class="">Gênero: {{ user.gender }}</p>
          <button @click="editUser(user)" class="edit-button">Editar</button>
          <button @click="deleteUser(user.id)" class="delete-button">Excluir</button>
        </div>
        <div style="margin-top: 1%" v-if="user.isEditing">
          <input  style="width: 20%; height: 37px;" v-model="user.username" placeholder="Username">
          <input  style="width: 20%; height: 37px;" v-model="user.first_name" placeholder="Nome">
          <input  style="width: 20%; height: 37px;" v-model="user.last_name" placeholder="Sobrenome">
          <input  style="width: 20%; height: 37px;" v-model="user.gender" placeholder="Gênero">
          <button @click="saveUser(user)" class="save-button">Salvar</button>
          <button @click="cancelEdit(user)" class="delete-button">Cancelar</button>
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
      users: [],
    };
  },
  methods: {
    async saveUser(user) {
      console.log(user.id)
      try {
        const response = await fetch(`http://localhost:8000/users/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: user.id,
            username: user.username,
            first_name: user.first_name,
            last_name: user.last_name,
            gender: user.gender,
            status: '1'
          }),
        });

        if (response.ok) {
          // Atualização bem-sucedida, você pode atualizar as informações no cliente
          // Certifique-se de atualizar cada campo do agendamento com base nos valores editados
          user.username = user.username;
          user.first_name = user.first_name;
          user.last_name = user.last_name;
          user.gender = user.gender;
          user.status = user.status;


          // Desative o modo de edição
          user.isEditing = false;
        } else {
          console.error('Erro ao atualizar o agendamento.');
        }
      } catch (error) {
        console.error('Erro ao atualizar o agendamento:', error);
      }
    },
    editUser(user) {
      user.isEditing = true;
    },
    cancelEdit(user) {
      // Cancela a edição, definindo isEditing como false
      user.isEditing = false;
    },
    async deleteUser(user) {
      try {
        const response = await fetch(`http://localhost:8000/users/${user}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          // Atualize a lista de agendamentos após a exclusão bem-sucedida
          this.fetchUsers();
        } else {
          console.error('Erro ao excluir usuário.');
        }
      } catch (error) {
        console.error('Erro ao excluir usuário:', error);
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
  },
  mounted() {
    this.fetchUsers();
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

.save-button {
  margin-right: 1%;
  margin-left: 1%;
  color: #fff;
  background-color: #15a605;
  border-color: #15a605;
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
.custom-select>.form-control {
  position: relative;
  -webkit-box-flex: 1;
  -ms-flex: 1 1 auto;
  flex: 1 1 auto;
  width: 1%;
  margin-bottom: 0;
}
</style>
