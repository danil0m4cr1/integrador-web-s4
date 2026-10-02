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
                        Email ou senha inválidos, tente novamente!
                    </p>
                    <div class="submit-button">
                        <input type="submit" value="Logar">
                    </div>
                    <router-link class="link" to="/register">Não tem conta? Cadastre-se</router-link>
                </form>
            </div>
        </div>
        
    </section>
</template>

<script setup>
import {ref} from 'vue';
import {useRouter} from 'vue-router';

const router = useRouter();

const email = ref('');
const pass = ref('');
const loginErr = ref(false);

function login(){   
    console.log(email.value);
    console.log(pass.value);

    if(email.value == "admin@teste.com" && pass.value == "admin"){
        loginErr.value = false;
        router.push("/home");
    } else {
        loginErr.value = true;
    }
}

</script>