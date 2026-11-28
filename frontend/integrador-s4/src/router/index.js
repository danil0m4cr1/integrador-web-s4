
import { createRouter, createWebHistory } from 'vue-router';

import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Home from '../views/Home.vue';
import Dashboard from '../views/Dashboard.vue';
import HistoryActive from '../views/HistoryActive.vue';
import OrdemServico from '../views/OrdemServico.vue';
import Ativos from '../views/Ativos.vue';
import AtivoDetalhes from '../views/AtivoDetalhes.vue';

// Verifica se o JWT existe e ainda não expirou
function tokenValido(token) {
    if (!token || token === 'undefined' || token === 'null') {
        return false;
    }

    try {
        const partes = token.split('.');

        if (partes.length !== 3) {
            return false;
        }

        const payloadBase64 = partes[1]
            .replace(/-/g, '+')
            .replace(/_/g, '/');

        const payload = JSON.parse(atob(payloadBase64));

        if (!payload.exp) {
            return false;
        }

        const expiracao = payload.exp * 1000;

        return Date.now() < expiracao;

    } catch (error) {
        return false;
    }
}

function encerrarSessao() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
}

const routes = [
    {
        path: '/',
        component: Login,
        meta: { guestOnly: true }
    },
    {
        path: '/cadastro',
        component: Register,
        meta: { guestOnly: true }
    },
    {
        path: '/home',
        component: Home,
        meta: { requiresAuth: true }
    },
    {
        path: '/ativos',
        component: Ativos,
        meta: { requiresAuth: true }
    },
    {
        path: '/ativos/:id',
        name: 'AtivoDetalhes',
        component: AtivoDetalhes,
        meta: { requiresAuth: true }
    },
    {
        path: '/historico',
        component: HistoryActive,
        meta: { requiresAuth: true }
    },
    {
        path: '/dashboard',
        component: Dashboard,
        meta: { requiresAuth: true }
    },
    {
        path: '/servicos',
        component: OrdemServico,
        meta: { requiresAuth: true }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

// Proteção global das rotas
router.beforeEach((to) => {
    const token = localStorage.getItem('access');
    const autenticado = tokenValido(token);

    // Token expirado ou inválido
    if (token && !autenticado) {
        encerrarSessao();
    }

    // Usuário sem sessão tentando acessar uma página protegida
    if (to.meta.requiresAuth && !autenticado) {
        return '/';
    }

    // Usuário autenticado tentando acessar login ou cadastro
    if (to.meta.guestOnly && autenticado) {
        return '/home';
    }

    return true;
});

// Monitoramento automático da expiração do token
setInterval(() => {
    const token = localStorage.getItem('access');

    if (token && !tokenValido(token)) {
        encerrarSessao();

        if (router.currentRoute.value.path !== '/') {
            router.replace('/');
        }
    }
}, 5000);

// Detecta logout realizado em outra aba
window.addEventListener('storage', (event) => {
    if (event.key === 'access' && !event.newValue) {
        router.replace('/');
    }
});

export default router;
