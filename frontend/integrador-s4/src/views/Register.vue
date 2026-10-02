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
                    <div class="submit-button">
                        <input type="submit" value="Cadastrar">
                    </div>
                    <router-link class="link" to="/">Já tem conta? Entrar</router-link>
                </form>
            </div>
        </div>
        
    </section>
</template>

<script setup>
import {ref} from 'vue';

const email = ref('');
const pass = ref('');
const confirmpass = ref('');

function register(){
    console.log(email.value);
    console.log(pass.value);
    console.log(confirmpass.value);
}

</script>