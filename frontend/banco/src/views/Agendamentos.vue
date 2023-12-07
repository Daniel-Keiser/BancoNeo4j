<template>
  <div class="container">
    <RouterLink class="create-button" to="/novo_agendamento">Criar Agendamento</RouterLink>

    <ul class="appointment-list">
      <li v-for="appointment in appointments" :key="appointment.id" class="appointment-item">
        <div class="info">
          <p class="patient">Paciente: {{ appointment.patient_username }}</p>
          <p class="doctor">Médico: {{ appointment.doctor_username }}</p>
          <p class="specialty">Especialidade: {{ appointment.specialty_name }}</p>
          <p class="datetime">Data e Hora: {{ appointment.appointment_datetime }}</p>
          <p class="status">Status: {{ appointment.status_name }}</p>
          <p class="observations">Observações: {{ appointment.observations }}</p>
          <p class="duration">Duração: {{ appointment.duration }}</p>
          <button @click="editAppointment(appointment)" class="edit-button">Editar</button>
          <button @click="deleteAppointment(appointment.appointment_id)" class="delete-button">Excluir</button>
        </div>
        <div style="margin-top: 1%" v-if="appointment.isEditing">
          <select style="width: 20%; height: 37px;" id="statusSelect" v-model="appointment.status_id" class="custom-select">
            <option v-for="statu in status" :key="statu.id" :value="statu.id">
              {{ statu.name }}
            </option>
          </select>
          <input style="width: 20%; height: 37px;" class="custom-text" v-model="appointment.observations" placeholder="Observações">
          <input style="width: 20%; height: 37px;" class="custom-text" v-model="appointment.duration" placeholder="Duração">
          <button @click="saveAppointment(appointment)" class="save-button">Salvar</button>
          <button @click="cancelEdit(appointment)" class="delete-button">Cancelar</button>
        </div>
      </li>
    </ul>

  </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router'

export default {
  name: 'Agendamentos',
  data() {
    return {
      appointments: [],
    };
  },
  methods: {
    async saveAppointment(appointment) {
      console.log(appointment)
      try {
        const response = await fetch(`http://localhost:8000/medical_appointments/${appointment.appointment_id}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            patient_id: appointment.patient_id,
            doctor_id: appointment.doctor_id,
            specialty_id:appointment.specialty_id,
            appointment_datetime: appointment.appointment_datetime,
            status_id: appointment.status_id,
            observations: appointment.observations,
            duration: appointment.duration,
          }),
        });

        if (response.ok) {
          // Atualização bem-sucedida, você pode atualizar as informações no cliente
          // Certifique-se de atualizar cada campo do agendamento com base nos valores editados
          appointment.status_id = appointment.status_id;
          appointment.observations = appointment.observations;
          appointment.duration = appointment.duration;
          appointment.patient_id = appointment.patient_id,
          appointment.doctor_id = appointment.doctor_id,
          appointment.specialty_id = appointment.specialty_id,

          // Desative o modo de edição
          appointment.isEditing = false;
          this.fetchAppointments();
        } else {
          console.error('Erro ao atualizar o agendamento.');
        }
      } catch (error) {
        console.error('Erro ao atualizar o agendamento:', error);
      }
    },
    editAppointment(appointment) {
      appointment.isEditing = true;
    },
    cancelEdit(appointment) {
      // Cancela a edição, definindo isEditing como false
      appointment.isEditing = false;
    },
    async deleteAppointment(appointmentId) {
      try {
        const response = await fetch(`http://localhost:8000/medical_appointments/${appointmentId}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          // Atualize a lista de agendamentos após a exclusão bem-sucedida
          this.fetchAppointments();
        } else {
          console.error('Erro ao excluir agendamento.');
        }
      } catch (error) {
        console.error('Erro ao excluir agendamento:', error);
      }
    },
    async fetchAppointments() {
      try {
        const response = await fetch('http://localhost:8000/medical_appointments', { method: 'GET' });
        if (response.ok) {
          const data = await response.json();
          this.appointments = data;
        } else {
          console.error('Erro ao buscar agendamentos.');
        }
      } catch (error) {
        console.error('Erro ao buscar agendamentos:', error);
      }
    },
    async fetchStatus() {
      try {
        const response = await fetch('http://localhost:8000/appointment-statuses', { method: 'GET' });
        if (response.ok) {
          const data = await response.json();
          this.status = data;
        } else {
          console.error('Erro ao buscar especialidades.');
        }
      } catch (error) {
        console.error('Erro ao buscar especialidades:', error);
      }
    },
  },
  mounted() {
    this.fetchAppointments();
    this.fetchStatus();
  },
};
</script>

<style scoped>
  /* Estilos para a lista de compromissos */
.appointment-list {
  list-style-type: none;
  padding: 0;
}

.appointment-item {
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
