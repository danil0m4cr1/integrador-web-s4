<template>
    <section class="login-section">

        <div class="login-left-container">
            <img src="/logo-tracklog.png" alt="Logo da TrackLog">
        </div>

        <div class="login-right-container">
            <div class="login-container">
                <form action=""> 
                    <h2>Login</h2>
                    <div class="input-label email-input">
                        <label for="email">Email</label>
                        <input type="email" placeholder="Digite seu email">
                    </div>
                    <div class="input-label password-input">
                        <label for="password">Senha</label>
                        <input type="password" placeholder="******">
                    </div>
                    <div class="submit-button">
                        <input type="submit" value="Logar">
                    </div>
                    <router-link>Não tem conta? Cadastre-se</router-link>
                </form>
            </div>
        </div>
        
    </section>
</template>