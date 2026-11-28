
<template>
    <section class="flex w-full min-h-screen h-screen max-[769px]:h-auto max-[769px]:min-h-screen max-[769px]:flex-col max-[769px]:justify-center max-[769px]:items-center max-[769px]:py-6">

        <!-- LADO ESQUERDO -->
        <div class="w-1/2 h-full flex justify-center items-center max-[769px]:w-full max-[769px]:h-auto max-[769px]:mb-4">

            <img
                src="/logo-tracklog.png"
                alt="Logo da TrackLog"
                class="w-[400px] h-[300px] object-contain max-[1024px]:w-[320px] max-[1024px]:h-[240px] max-[769px]:w-[280px] max-[769px]:h-[180px] max-[480px]:w-[220px] max-[480px]:h-[140px]"
            >

        </div>

        <!-- LADO DIREITO -->
        <div class="w-1/2 h-full flex justify-center items-center max-[769px]:w-full max-[769px]:h-auto">

            <div class="w-[90%] h-[90%] bg-[rgb(37,73,107)] flex justify-center max-[1024px]:w-[95%] max-[1024px]:h-[95%] max-[769px]:w-[90%] max-[769px]:h-auto max-[769px]:min-h-[520px] max-[769px]:py-8 max-[480px]:w-[94%] max-[480px]:min-h-[460px] max-[480px]:py-6">

                <form
                    @submit.prevent="login"
                    class="text-white w-full flex flex-col items-center"
                >

                    <h2 class="pt-[98px] pb-[40px] text-[32px] max-[1024px]:pt-[70px] max-[1024px]:pb-[30px] max-[769px]:pt-6 max-[769px]:pb-6 max-[769px]:text-[28px] max-[480px]:text-[26px]">
                        LOGIN
                    </h2>

                    <!-- EMAIL -->
                    <div class="flex flex-col gap-[10px] w-[60%] py-[20px] max-[1024px]:w-[75%] max-[769px]:w-[75%] max-[480px]:w-[85%] max-[480px]:py-3">

                        <label
                            for="email"
                            class="text-[24px] max-[769px]:text-[20px] max-[480px]:text-[18px]"
                        >
                            Email
                        </label>

                        <input
                            id="email"
                            type="email"
                            v-model="email"
                            required
                            class="h-[40px] px-[15px] text-[18px] outline-none border-0 border-b border-b-white bg-transparent text-white max-[480px]:text-[16px]"
                        >

                    </div>

                    <!-- SENHA -->
                    <div class="flex flex-col gap-[10px] w-[60%] py-[20px] max-[1024px]:w-[75%] max-[769px]:w-[75%] max-[480px]:w-[85%] max-[480px]:py-3">

                        <label
                            for="password"
                            class="text-[24px] max-[769px]:text-[20px] max-[480px]:text-[18px]"
                        >
                            Senha
                        </label>

                        <input
                            id="password"
                            type="password"
                            v-model="pass"
                            required
                            class="h-[40px] px-[15px] text-[18px] outline-none border-0 border-b border-b-white bg-transparent text-white max-[480px]:text-[16px]"
                        >

                    </div>

                    <!-- ERRO -->
                    <p
                        v-if="loginErr"
                        class="text-red-300 text-[16px] text-center px-4 max-[480px]:text-[15px]"
                    >
                        {{ mensagemErro }}
                    </p>

                    <!-- BOTÃO -->
                    <div class="pt-[25px] pb-[22px] max-[769px]:pt-5 max-[480px]:pb-4">

                        <input
                            type="submit"
                            :value="carregando ? 'Entrando...' : 'Logar'"
                            :disabled="carregando"
                            class="appearance-none w-[180px] h-[60px] border-0 cursor-pointer bg-white text-black rounded-[15px] font-bold text-[24px] hover:bg-[#dcdcdc] transition-all duration-[400ms] disabled:opacity-60 disabled:cursor-not-allowed max-[480px]:w-[160px] max-[480px]:h-[52px] max-[480px]:text-[20px]"
                        >

                    </div>

                    <!-- LINK CADASTRO -->
                    <router-link
                        class="cursor-pointer text-white no-underline hover:underline text-center px-3 max-[480px]:text-[14px]"
                        to="/cadastro"
                    >
                        Não tem conta? Cadastre-se
                    </router-link>

                </form>

            </div>

        </div>

    </section>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const router = useRouter();

const email = ref('');
const pass = ref('');
const loginErr = ref(false);
const mensagemErro = ref('');
const carregando = ref(false);

async function login() {
    loginErr.value = false;
    mensagemErro.value = '';

    if (!email.value.trim() || !pass.value) {
        loginErr.value = true;
        mensagemErro.value = 'Informe seu e-mail e sua senha.';
        return;
    }

    carregando.value = true;

    try {
        const response = await api.post('/usuarios/login/', {
            email: email.value.trim().toLowerCase(),
            password: pass.value,
        });

        const dados = response.data;

        // Valida os dados obrigatórios.
        if (!dados.access || !dados.refresh) {
            throw new Error('A API não retornou os tokens de autenticação.');
        }

        if (!dados.id || !dados.email) {
            console.error('Dados do usuário ausentes:', {
                id: dados.id,
                email: dados.email
            });

            throw new Error(
                'A API não retornou o ID ou o e-mail do usuário. Verifique a view de login no Django.'
            );
        }

        // Salva os dados de autenticação.
        localStorage.setItem('access', dados.access);
        localStorage.setItem('refresh', dados.refresh);
        localStorage.setItem('usuario_id', String(dados.id));
        localStorage.setItem('usuario_email', dados.email);

        

        await router.push('/home');

    } catch (error) {
        loginErr.value = true;

        if (error.response?.status === 401) {
            mensagemErro.value = 'E-mail ou senha inválidos.';
        } else if (error.message?.includes('API não retornou')) {
            mensagemErro.value = error.message;
        } else if (error.response?.data?.detail) {
            mensagemErro.value = error.response.data.detail;
        } else {
            mensagemErro.value =
                'Não foi possível conectar ao servidor.';
        }

        console.error(
            'Erro no login:',
            error.response?.data || error.message
        );

    } finally {
        carregando.value = false;
    }
}
</script>
