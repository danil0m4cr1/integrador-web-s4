<template>
    <div class="min-h-screen bg-white">
        <Navbar />

        <main class="flex flex-col items-center gap-10 mt-[80px] px-4">

            <h1 class="text-4xl font-bold">Bem vindo a TrackLog</h1>

            <button
                class="w-full max-w-[520px] h-28
                       border-2 border-[#8fcf8f]
                       rounded-2xl text-2xl font-bold
                       text-black hover:bg-[#E5F8EC]/30
                       transition duration-200 cursor-pointer"
                @click="$router.push('historico')"
            >
                ÚLTIMAS MOVIMENTAÇÕES
            </button>

            <button
                class="w-full max-w-[520px] h-28
                       border-2 border-[#8fcf8f]
                       rounded-2xl text-2xl font-bold
                       text-black hover:bg-[#E5F8EC]/30
                       transition duration-200 cursor-pointer"
                @click="$router.push('dashboard')"
            >
                DASHBOARD
            </button>

        </main>
    </div>
</template>

<script>
import Navbar from '../components/navbarVue.vue'

export default {
    name: "Home",
    components: {
        Navbar
    }
}
</script>