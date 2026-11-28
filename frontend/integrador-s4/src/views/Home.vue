
<template>
    <div class="min-h-screen bg-white">
        <Navbar />

        <main class="mx-auto flex w-full max-w-7xl flex-col gap-10 px-4 py-12 sm:px-6 lg:px-8">

            <!-- TÍTULO -->
            <section class="text-center">
                <h1 class="text-3xl font-bold text-gray-900 sm:text-4xl">
                    Bem-vindo à TrackLog
                </h1>
            </section>

            <!-- CARDS -->
            <section class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">

                <!-- ATIVOS -->
                <button
                    @click="$router.push('/ativos')"
                    class="group flex min-h-52 flex-col items-center justify-center cursor-pointer gap-4 rounded-2xl border-2 border-[#8fcf8f] bg-white p-6 text-center transition duration-200 hover:-translate-y-1 hover:bg-[#E5F8EC]/30 hover:shadow-lg"
                >
                    <div class="flex h-16 w-16 items-center justify-center rounded-full bg-[#E5F8EC] text-[#398D50]">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                        </svg>
                    </div>

                    <div>
                        <h2 class="text-xl font-bold text-gray-900">Ativos</h2>
                    </div>
                </button>

                <!-- ORDENS DE SERVIÇO -->
                <button
                    @click="$router.push('/servicos')"
                    class="group flex min-h-52 flex-col items-center justify-center cursor-pointer gap-4 rounded-2xl border-2 border-[#8fcf8f] bg-white p-6 text-center transition duration-200 hover:-translate-y-1 hover:bg-[#E5F8EC]/30 hover:shadow-lg"
                >
                    <div class="flex h-16 w-16 items-center justify-center rounded-full bg-[#E5F8EC] text-[#398D50]">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 7h6m-6 4h6" />
                        </svg>
                    </div>

                    <div>
                        <h2 class="text-xl font-bold text-gray-900">Ordens de Serviço</h2>
                    </div>
                </button>

                <!-- DASHBOARD -->
                <button
                    @click="$router.push('/dashboard')"
                    class="group flex min-h-52 flex-col items-center justify-center cursor-pointer gap-4 rounded-2xl border-2 border-[#8fcf8f] bg-white p-6 text-center transition duration-200 hover:-translate-y-1 hover:bg-[#E5F8EC]/30 hover:shadow-lg"
                >
                    <div class="flex h-16 w-16 items-center justify-center rounded-full bg-[#E5F8EC] text-[#398D50]">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v18h18M18 17V9m-5 8V5m-5 12v-5" />
                        </svg>
                    </div>

                    <div>
                        <h2 class="text-xl font-bold text-gray-900">Dashboard</h2>
                    </div>
                </button>

                <!-- HISTÓRICO -->
                <button
                    @click="$router.push('/historico')"
                    class="group flex min-h-52 flex-col items-center justify-center cursor-pointer gap-4 rounded-2xl border-2 border-[#8fcf8f] bg-white p-6 text-center transition duration-200 hover:-translate-y-1 hover:bg-[#E5F8EC]/30 hover:shadow-lg"
                >
                    <div class="flex h-16 w-16 items-center justify-center rounded-full bg-[#E5F8EC] text-[#398D50]">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 2m6-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>

                    <div>
                        <h2 class="text-xl font-bold text-gray-900">Histórico</h2>
                    </div>
                </button>

            </section>
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
