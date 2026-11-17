import { createRouter, createWebHistory } from 'vue-router';

import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Home from "../views/Home.vue";
import Ra from "../views/Ra.vue";
import Dashboard from "../views/Dashboard.vue";
import HistoryActive from "../views/HistoryActive.vue";
import OrdemServico from '../views/OrdemServico.vue';

const routes = [
    {
        path: "/",
        component: Login
    },
    {
        path: "/cadastro",
        component: Register
    },
    {
        path: "/home",
        component: Home
    },
    {
        path: "/ra",
        component: Ra
    },
    {
        path: "/historico",
        component: HistoryActive
    },
    {
        path: "/dashboard",
        component: Dashboard
    },
    {
        path: "/servicos",
        component: OrdemServico
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;