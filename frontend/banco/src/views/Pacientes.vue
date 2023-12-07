<template>
  <div class="container">
    <RouterLink class="create-button" to="/novo_paciente">Criar Paciente</RouterLink>

    <ul class="patient-list">
      <li v-for="patient in patients" :key="patient.id" class="patient-item">
        <div class="info">
          <p class="patient">Usuário: {{ patient.username }}</p>
          <p class="">Nome: {{ patient.first_name }} {{ patient.last_name }}</p>
          <p class="">Endereço: {{ patient.address }}</p>
          <p class="">Telefone: {{ patient.phone_number }}</p>
          <p class="">Histórico Médico: {{ patient.medical_history }}</p>
          <p class="">Idade: {{ patient.age }}</p>
          <button @click="editPatient(patient)" class="edit-button">Editar</button>
          <button @click="deletePatient(patient.id)" class="delete-button">Excluir</button>
        </div>
        <div  style="margin-top: 1%" v-if="patient.isEditing">
          <input  style="width: 20%; height: 37px;"  v-model="patient.age" placeholder="Idade">
          <input  style="width: 20%; height: 37px;"  v-model="patient.address" placeholder="Endereço">
          <input  style="width: 20%; height: 37px;"  v-model="patient.phone_number" placeholder="Telefone">
          <input  style="width: 20%; height: 37px;"  v-model="patient.medical_history" placeholder="Histórico Médico">
          <button @click="savePatient(patient)" class="save-button">Salvar</button>
          <button @click="cancelEdit(patient)" class="delete-button">Cancelar</button>
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
      patients: [],
    };
  },
  methods: {
    async savePatient(patient) {
      console.log('chegando')
      try {
        const response = await fetch(`http://localhost:8000/patients/${patient.patient_id}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            age: patient.age,
            medical_history: patient.medical_history,
            phone_number: patient.phone_number,
            address: patient.address,
            contact_emergency: patient.contact_emergency,
          }),
        });

        if (response.ok) {
          // Atualização bem-sucedida, você pode atualizar as informações no cliente
          // Certifique-se de atualizar cada campo do agendamento com base nos valores editados
          patient.age = patient.age;
          patient.medical_history = patient.medical_history;
          patient.phone_number = patient.phone_number;
          patient.address = patient.address;
          patient.contact_emergency = patient.contact_emergency;


          // Desative o modo de edição
          patient.isEditing = false;
        } else {
          console.error('Erro ao atualizar o agendamento.');
        }
      } catch (error) {
        console.error('Erro ao atualizar o agendamento:', error);
      }
    },
    editPatient(patient) {
      patient.isEditing = true;
    },
    cancelEdit(patient) {
      // Cancela a edição, definindo isEditing como false
      patient.isEditing = false;
    },
    async deletePatient(patient) {
      try {
        const response = await fetch(`http://localhost:8000/patients/${patient.patient_id}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          // Atualize a lista de agendamentos após a exclusão bem-sucedida
          this.fetchPatient();
        } else {
          console.error('Erro ao excluir agendamento.');
        }
      } catch (error) {
        console.error('Erro ao excluir agendamento:', error);
      }
    },
    async fetchPatient() {
      try {
        const response = await fetch('http://localhost:8000/patients', { method: 'GET' });
        if (response.ok) {
          const data = await response.json();
          this.patients = data;
          console.log(this.patients)
        } else {
          console.error('Erro ao buscar agendamentos.');
        }
      } catch (error) {
        console.error('Erro ao buscar agendamentos:', error);
      }
    },
  },
  mounted() {
    this.fetchPatient();
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
