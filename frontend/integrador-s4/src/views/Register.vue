
<template>
    <section class="w-full h-screen flex max-[769px]:flex-col max-[769px]:justify-center max-[769px]:items-center max-[769px]:h-auto max-[769px]:min-h-screen">

        <!-- LADO ESQUERDO -->
        <div class="w-1/2 h-full flex justify-center items-center max-[769px]:w-full max-[769px]:h-auto max-[769px]:py-2">

            <img
                src="/logo-tracklog.png"
                alt="Logo da TrackLog"
                class="w-[400px] h-[300px] object-contain max-[1024px]:w-[320px] max-[1024px]:h-[240px] max-[769px]:w-[280px] max-[769px]:h-[160px] max-[480px]:w-[220px] max-[480px]:h-[130px]"
            >

        </div>

        <!-- LADO DIREITO -->
        <div class="w-1/2 h-full flex justify-center items-center max-[769px]:w-full max-[769px]:h-auto">

            <div class="w-[90%] h-[90%] bg-[rgb(37,73,107)] flex justify-center max-[1024px]:w-[95%] max-[769px]:w-[90%] max-[769px]:h-auto max-[480px]:w-[94%]">

                <form
                    @submit.prevent="register"
                    class="text-white w-full flex flex-col items-center"
                >

                    <!-- TÍTULO -->
                    <h2 class="pt-[48px] pb-[20px] text-[32px] max-[1024px]:pt-[35px] max-[769px]:pt-[25px] max-[769px]:pb-[15px] max-[769px]:text-[28px] max-[480px]:text-[26px]">

                        CADASTRO

                    </h2>

                    <!-- EMAIL -->
                    <div class="flex flex-col gap-[10px] w-[60%] py-[20px] max-[1024px]:w-[75%] max-[769px]:w-[75%] max-[769px]:py-[15px] max-[480px]:w-[85%] max-[480px]:py-[12px]">

                        <label
                            for="email"
                            class="text-[24px] max-[769px]:text-[21px] max-[480px]:text-[18px]"
                        >
                            Email
                        </label>

                        <input
                            id="email"
                            type="email"
                            v-model="email"
                            class="h-[40px] px-[15px] text-[18px] outline-none border-0 border-b border-b-white bg-transparent text-white max-[480px]:text-[16px]"
                        >

                    </div>

                    <!-- SENHA -->
                    <div class="flex flex-col gap-[10px] w-[60%] py-[20px] max-[1024px]:w-[75%] max-[769px]:w-[75%] max-[769px]:py-[15px] max-[480px]:w-[85%] max-[480px]:py-[12px]">

                        <label
                            for="password"
                            class="text-[24px] max-[769px]:text-[21px] max-[480px]:text-[18px]"
                        >
                            Senha
                        </label>

                        <input
                            id="password"
                            type="password"
                            v-model="pass"
                            class="h-[40px] px-[15px] text-[18px] outline-none border-0 border-b border-b-white bg-transparent text-white max-[480px]:text-[16px]"
                        >

                    </div>

                    <!-- CONFIRMAR SENHA -->
                    <div class="flex flex-col gap-[10px] w-[60%] py-[20px] max-[1024px]:w-[75%] max-[769px]:w-[75%] max-[769px]:py-[15px] max-[480px]:w-[85%] max-[480px]:py-[12px]">

                        <label
                            for="confirm-password"
                            class="text-[24px] max-[769px]:text-[21px] max-[480px]:text-[18px]"
                        >
                            Confirmar senha
                        </label>

                        <input
                            id="confirm-password"
                            type="password"
                            v-model="confirmpass"
                            class="h-[40px] px-[15px] text-[18px] outline-none border-0 border-b border-b-white bg-transparent text-white max-[480px]:text-[16px]"
                        >

                    </div>

                    <!-- MENSAGEM DE ERRO -->
                    <p
                        v-if="erro"
                        class="text-red-500 text-[18px] text-center px-3 max-[480px]:text-[15px]"
                    >
                        {{ erro }}
                    </p>

                    <!-- MENSAGEM DE SUCESSO -->
                    <p
                        v-if="sucesso"
                        class="text-green-500 text-[18px] text-center px-3 max-[480px]:text-[15px]"
                    >
                        {{ sucesso }}
                    </p>

                    <!-- BOTÃO -->
                    <div class="pt-[25px] pb-[22px] max-[769px]:pt-[20px] max-[480px]:pb-[18px]">

                        <input
                            type="submit"
                            :value="carregando ? 'Cadastrando...' : 'Cadastrar'"
                            :disabled="carregando"
                            class="appearance-none w-[180px] h-[60px] border-0 cursor-pointer bg-white text-black rounded-[15px] font-bold text-[24px] hover:bg-[rgb(220,220,220)] transition-all duration-[400ms] disabled:opacity-60 disabled:cursor-not-allowed max-[480px]:w-[160px] max-[480px]:h-[55px] max-[480px]:text-[20px]"
                        >

                    </div>

                    <!-- LINK LOGIN -->
                    <router-link
                        class="cursor-pointer text-white no-underline hover:underline mb-8 max-[480px]:text-[14px]"
                        to="/"
                    >
                        Já tem conta? Entrar
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
const confirmpass = ref('');

const erro = ref('');
const sucesso = ref('');
const carregando = ref(false);

async function register() {
    erro.value = '';
    sucesso.value = '';

    if (pass.value !== confirmpass.value) {
        erro.value = 'As senhas não coincidem.';
        return;
    }

    if (!email.value || !pass.value) {
        erro.value = 'Preencha todos os campos.';
        return;
    }

    carregando.value = true;

    try {
        const response = await api.post(
            `${import.meta.env.VITE_API_URL}/api/usuarios/cadastrar/`,
            {
                email: email.value,
                password: pass.value,
            }
        );

        sucesso.value = 'Cadastro realizado com sucesso!';

        console.log('Usuário cadastrado:', response.data);

        email.value = '';
        pass.value = '';
        confirmpass.value = '';

        setTimeout(() => {
            router.push('/');
        }, 1500);

    } catch (error) {
        const data = error.response?.data;

        if (data?.email) {
            erro.value = Array.isArray(data.email)
                ? data.email[0]
                : data.email;
        } else if (data?.detail) {
            erro.value = data.detail;
        } else {
            erro.value =
                'Não foi possível realizar o cadastro. Verifique a conexão com o servidor.';
        }

        console.error('Erro no cadastro:', data || error.message);

    } finally {
        carregando.value = false;
    }
}

</script>
