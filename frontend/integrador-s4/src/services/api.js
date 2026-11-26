
import axios from 'axios';

const api = axios.create({
    baseURL: `${import.meta.env.VITE_API_URL}/api`,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Adiciona o token JWT automaticamente nas requisições
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// Trata respostas de erro da API
api.interceptors.response.use(
    (response) => response,
    (error) => {
        const status = error.response?.status;
        const url = error.config?.url || '';

        // Não encerra a sessão quando o erro acontece no próprio login
        const isLoginRequest = url.includes('/usuarios/login/');

        if (status === 401 && !isLoginRequest) {
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');

            // Redireciona para o login
            if (window.location.pathname !== '/') {
                window.location.replace('/');
            }
        }

        return Promise.reject(error);
    }
);

export default api;
