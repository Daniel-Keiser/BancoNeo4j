document.addEventListener("DOMContentLoaded", () => {
    const appointmentList = document.getElementById("appointment-list");

    // Função para buscar agendamentos da API
    const fetchAppointments = async () => {
        try {
            const response = await fetch("http://localhost:8000/medical_appointments");
            if (!response.ok) {
                throw new Error("Erro ao buscar agendamentos.");
            }

            const data = await response.json();
            displayAppointments(data);
        } catch (error) {
            console.error(error);
        }
    };

    // Função para exibir os agendamentos na página
    const displayAppointments = (appointments) => {
        appointmentList.innerHTML = "";

        appointments.forEach((appointment) => {
            const listItem = document.createElement("li");
            listItem.textContent = `ID: ${appointment.id}, Paciente: ${appointment.patient_id}, Médico: ${appointment.doctor_id}`;
            appointmentList.appendChild(listItem);
        });
    };

    // Inicialize a busca de agendamentos ao carregar a página
    fetchAppointments();
});
