import { http } from './config'

export default {
    listar: () => {
        return http.get('medical_appointments')
            .then(response => {
                console.log('URL da solicitação:', response.config.url);
                console.log('Resposta do servidor:', response.data);
                return response;
            })
            .catch(error => {
                console.error('Erro ao buscar dados da API:', error);
                throw error;
            });
    }
}
