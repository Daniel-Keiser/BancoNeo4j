<template>
  <div class="container">
   
    <h2>Criar Novo Agendamento</h2>
    <form @submit.prevent="submitAppointment">
        <div class="form-group">
          <label for="patientSelect">Selecione um Paciente:</label>
          <select id="patientSelect" v-model="selectedPatientId" class="select-field">
            <option v-for="patient in patients" :key="patient.id" :value="patient.patient_id">
              {{ patient.username }}
            </option>
          </select>
        </div>
      <div class="form-group">
        <label for="doctorSelect">Selecione um Médico:</label>
        <select id="doctorSelect" v-model="selectedDoctorId" class="select-field">
          <option v-for="doctor in doctors" :key="doctor.id" :value="doctor.doctor_id">
            {{ doctor.username }}
          </option>
        </select>
      </div>
   
   
      <!-- Campo para mostrar a especialidade do médico -->
      <div class="form-group" v-if="selectedDoctorId">
        <label for="doctorSelect">Especialidade:</label>
        <input
            id="doctorSpecialty"
            type="text"
            class="form-control"
            v-model="selectedDoctorSpecialty"
            disabled >
      </div>
      <div class="form-group">
        <label for="appointment_datetime">Data e Hora do Agendamento</label>
        <input type="datetime-local" id="appointment_datetime" v-model="newAppointment.appointment_datetime" required>
      </div>
      <div class="form-group">
        <label for="statusSelect">Status da Consulta:</label>
        <select id="statusSelect" v-model="selectedStatusId" class="select-field">
          <option v-for="statu in status" :key="statu.id" :value="statu.id">
            {{ statu.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="observations">Observações</label>
        <textarea id="observations" v-model="newAppointment.observations"></textarea>
      </div>
      <div class="form-group">
        <label for="duration">Duração</label>
        <input type="text" id="duration" v-model="newAppointment.duration" required>
      </div>
      <button type="submit">Criar Agendamento</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'NewAppointment',
  data() {
    return {
      patients: [],
      doctors: [],
      status: [],
      selectedPatientId: null,
      selectedDoctorId: null,
      selectedSpecialtyId: null,
      selectedStatusId: null,
      newAppointment: {
        patient_id: null,
        doctor_id: null,
        specialty_id: null,
        appointment_datetime: null,
        status_id: null,
        observations: '',
        duration: ''
      }
    };
  },
  methods: {
    async submitAppointment() {
      try {
        const newAppointmentData = {
          patient_id: this.selectedPatientId,
          doctor_id: this.selectedDoctorId,
          specialty_id: '5', 
          appointment_datetime: this.newAppointment.appointment_datetime,
          status_id: this.selectedStatusId,
          observations: this.newAppointment.observations,
          duration: this.newAppointment.duration
        };

        // Faça a solicitação POST para o endpoint de criação de agendamento
        const response = await axios.post('http://localhost:8000/appointments', newAppointmentData);

        if (response.status === 201) {
          // O agendamento foi criado com sucesso, você pode redirecionar o usuário ou fazer outra ação
          this.$router.push('/agendamentos'); // Redirecionar de volta à lista de agendamentos
        }
      } catch (error) {
        console.error('Erro ao criar agendamento:', error);
      }
    },
    async fetchPatients() {
      try {
        const response = await fetch('http://localhost:8000/patients', { method: 'GET' });
        if (response.ok) {
          const data = await response.json();
          this.patients = data;
          console.log(this.patients)
        } else {
          console.error('Erro ao buscar pacientes.');
        }
      } catch (error) {
        console.error('Erro ao buscar pacientes:', error);
      }
    },
    async fetchDoctors() {
      try {
        const response = await fetch('http://localhost:8000/doctors', { method: 'GET' });
        if (response.ok) {
          const data = await response.json();
          this.doctors = data;
        } else {
          console.error('Erro ao buscar médicos.');
        }
      } catch (error) {
        console.error('Erro ao buscar médicos:', error);
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
    this.fetchPatients();
    this.fetchDoctors();
    this.fetchStatus();
  },
  computed: {
    selectedDoctorSpecialty() {
      // Implemente a lógica para obter a especialidade do médico selecionado
      const selectedDoctor = this.doctors.find(doctor => doctor.id === this.selectedDoctorId);
      this.selectedSpecialtyId = selectedDoctor.specialization_id
      console.log(this.selectedSpecialtyId)
      return selectedDoctor ? selectedDoctor.specialization_name : '';
    },
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

