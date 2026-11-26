<template>
    <section>
        <nav class="navbar">
            <div class="navbar-container">

                <a href="#" class="navbar-brand">
                    <img
                        src="/logo-tracklog-minimalist.png"
                        alt="Logo Tracklog"
                        class="navbar-logo"
                    />
                </a>

                <ul class="navbar-menu">
                    <li>
                        <router-link to="/home">Home</router-link>
                    </li>
                    <li>
                        <router-link to="/dashboard">Dashboard</router-link>
                    </li>
                    <li>
                        <router-link to="/historico">Histórico</router-link>
                    </li>
                    <li>
                        <router-link to="/servicos">Serviços</router-link>
                    </li>
                </ul>

            </div>
        </nav>
    </section>
</template>

<script>
import router from '../router';

export default {
    name: 'Navbar'
}
</script>

<style scoped>
.navbar {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 80px;
    position: sticky;
    top: 0;
    background-color: rgb(143, 207, 143);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.25);
    z-index: 999;
}

.navbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    max-width: 1600px;
    padding: 0 40px;
    box-sizing: border-box;
}

.navbar-brand {
    display: flex;
    align-items: center;
    text-decoration: none;
}

.navbar-logo {
    display: block;
    width: 150px;
    height: auto;
    max-height: 65px;
    object-fit: contain;
}

.navbar-menu {
    display: flex;
    align-items: center;
    gap: 15px;
    list-style: none;
    padding: 0;
    margin: 0;
}

.navbar-menu li a {
    display: block;
    text-decoration: none;
    font-size: 18px;
    font-weight: 500;
    padding: 10px 18px;
    border-radius: 20px;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.navbar-menu li a:hover {
    color: #155b38;
    background-color: rgb(161, 231, 160);
    border-color: white;
}

@media (max-width: 600px) {
    .navbar-container {
        flex-direction: column;
        gap: 12px;
        padding: 12px;
    }

    .navbar-menu {
        flex-direction: column;
        justify-content: center;
        gap: 10px;
    }

    .navbar-menu li a {
        font-size: 24px;
        padding: 8px 10px;
    }
}
</style>