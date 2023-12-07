import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Agendamentos.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/agendamentos',
      name: 'agendamentos',
      component: () => import('../views/Agendamentos.vue')
    },
    {
      path: '/novo_agendamento',
      name: 'novo agendamento',
      component: () => import('@/components/NewAppointment.vue')
    },
    {
      path: '/novo_paciente',
      name: 'novo paciente',
      component: () => import('@/components/NewPatient.vue')
    },
    {
      path: '/novo_medico',
      name: 'novo medico',
      component: () => import('@/components/NewDoctor.vue')
    },
    {
      path: '/novo_status',
      name: 'novo status',
      component: () => import('@/components/NewStatus.vue')
    },
    {
      path: '/nova_especialidade',
      name: 'nova especialidade',
      component: () => import('@/components/NewSpecialty.vue')
    },
    {
      path: '/novo_usuario',
      name: 'novo usuario',
      component: () => import('@/components/NewUser.vue')
    },
    {
      path: '/pacientes',
      name: 'pacientes',
      component: () => import('../views/Pacientes.vue')
    },
    {
      path: '/medicos',
      name: 'medicos',
      component: () => import('../views/Medicos.vue')
    },
    {
      path: '/usuarios',
      name: 'usuarios',
      component: () => import('../views/Usuarios.vue')
    },
    {
      path: '/status',
      name: 'status',
      component: () => import('../views/Status.vue')
    },
    {
      path: '/especialidades',
      name: 'especialidades',
      component: () => import('../views/Especialidades.vue')
    }
  ]
})

export default router
