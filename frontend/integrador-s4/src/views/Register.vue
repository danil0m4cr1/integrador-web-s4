<template>
    <section class="register-section">

        <div class="register-left-container">
            <img src="/logo-tracklog.png" alt="Logo da TrackLog">
        </div>

        <div class="register-right-container">
            <div class="register-container">
                <form @submit.prevent="register"> 
                    <h2>CADASTRO</h2>
                    <div class="input-label email-input">
                        <label for="email">Email</label>
                        <input type="email" v-model="email">
                    </div>
                    <div class="input-label password-input">
                        <label for="password">Senha</label>
                        <input type="password" v-model="pass">
                    </div>
                    <div class="input-label confirm-password-input">
                        <label for="confirm-password">Confirmar senha</label>
                        <input type="password" v-model="confirmpass">
                    </div>
                    <p v-if="erro" class="error-msg-login">
                        {{ erro }}
                    </p>
                    <p v-if="sucesso" class="sucess-msg">
                        {{ sucesso }}
                    </p>
                    <div class="submit-button">
                        <input type="submit" 
                        :value="carregando ? 'Cadastrando...' : 'Cadastrar'"
                        :disabled="carregando">
                    </div>
                    <router-link class="link" to="/">Já tem conta? Entrar</router-link>
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
      '/usuarios/cadastrar/',
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