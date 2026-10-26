<template>
    <section class="login-section">

        <div class="login-left-container">
            <img src="/logo-tracklog.png" alt="Logo da TrackLog">
        </div>

        <div class="login-right-container">
            <div class="login-container">
                <form @submit.prevent="login"> 
                    <h2>LOGIN</h2>
                    <div class="input-label email-input">
                        <label for="email">Email</label>
                        <input type="email" v-model="email">
                    </div>
                    <div class="input-label password-input">
                        <label for="password">Senha</label>
                        <input type="password" v-model="pass">
                    </div>
                    <p v-if="loginErr" class="error-msg-login">
                        {{ mensagemErro }}
                    </p>
                    <div class="submit-button">
                        <input type="submit" 
                        :value="carregando ? 'Entrando...' : 'Logar'"
                        :disabled="carregando">
                    </div>
                    <router-link class="link" to="/register">Não tem conta? Cadastre-se</router-link>
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

    console.log('Login realizado:', response.data);

    // Redireciona após a confirmação do backend.
    await router.push('/home');

  } catch (error) {
    loginErr.value = true;

    if (error.response?.status === 401) {
      mensagemErro.value = 'E-mail ou senha inválidos.';
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