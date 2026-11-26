
<template>
    <section>
        <nav
            class="sticky top-0 z-[999] flex min-h-[80px] w-full items-center justify-center bg-[#8fcf8f] shadow-[0_5px_15px_rgba(0,0,0,0.25)]"
        >
            <div
                class="box-border flex w-full max-w-[1600px] items-center justify-between px-10 max-[600px]:flex-col max-[600px]:gap-3 max-[600px]:px-3 max-[600px]:py-3"
            >
                <!-- LOGO -->
                <router-link
                    to="/home"
                    class="flex items-center no-underline"
                >
                    <img
                        src="/logo-tracklog-minimalist.png"
                        alt="Logo Tracklog"
                        class="block h-auto max-h-[65px] w-[150px] object-contain"
                    />
                </router-link>

                <!-- MENU -->
                <ul
                    class="m-0 flex list-none items-center gap-[15px] p-0 max-[600px]:flex-col max-[600px]:justify-center max-[600px]:gap-[10px]"
                >
                    <li>
                        <router-link
                            to="/home"
                            class="block whitespace-nowrap rounded-[20px] px-[18px] py-[10px] text-[18px] font-medium text-[#155b38] no-underline transition-all duration-300 hover:bg-[#a1e7a0] hover:text-[#155b38] max-[600px]:px-[10px] max-[600px]:py-2 max-[600px]:text-2xl"
                        >
                            Home
                        </router-link>
                    </li>

                    <li>
                        <router-link
                            to="/ativos"
                            class="block whitespace-nowrap rounded-[20px] px-[18px] py-[10px] text-[18px] font-medium text-[#155b38] no-underline transition-all duration-300 hover:bg-[#a1e7a0] hover:text-[#155b38] max-[600px]:px-[10px] max-[600px]:py-2 max-[600px]:text-2xl"
                        >
                            Ativos
                        </router-link>
                    </li>

                    <li>
                        <router-link
                            to="/dashboard"
                            class="block whitespace-nowrap rounded-[20px] px-[18px] py-[10px] text-[18px] font-medium text-[#155b38] no-underline transition-all duration-300 hover:bg-[#a1e7a0] hover:text-[#155b38] max-[600px]:px-[10px] max-[600px]:py-2 max-[600px]:text-2xl"
                        >
                            Dashboard
                        </router-link>
                    </li>

                    <li>
                        <router-link
                            to="/historico"
                            class="block whitespace-nowrap rounded-[20px] px-[18px] py-[10px] text-[18px] font-medium text-[#155b38] no-underline transition-all duration-300 hover:bg-[#a1e7a0] hover:text-[#155b38] max-[600px]:px-[10px] max-[600px]:py-2 max-[600px]:text-2xl"
                        >
                            Histórico
                        </router-link>
                    </li>

                    <li>
                        <router-link
                            to="/servicos"
                            class="block whitespace-nowrap rounded-[20px] px-[18px] py-[10px] text-[18px] font-medium text-[#155b38] no-underline transition-all duration-300 hover:bg-[#a1e7a0] hover:text-[#155b38] max-[600px]:px-[10px] max-[600px]:py-2 max-[600px]:text-2xl"
                        >
                            Serviços
                        </router-link>
                    </li>

                    <!-- LOGOUT -->
                    <li>
                        <button
                            type="button"
                            @click="logout"
                            class="flex cursor-pointer items-center justify-center gap-2 whitespace-nowrap rounded-[20px] border-none bg-[#155b38] px-[18px] py-[10px] text-[17px] font-semibold text-white transition-all duration-300 hover:-translate-y-0.5 hover:bg-[#a32929] max-[600px]:text-xl"
                        >
                            <span>Sair</span>

                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="21"
                                height="21"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            >
                                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                                <polyline points="16 17 21 12 16 7" />
                                <line x1="21" y1="12" x2="9" y2="12" />
                            </svg>
                        </button>
                    </li>
                </ul>

            </div>
        </nav>
    </section>
</template>

<script>
import router from '../router'

export default {
    name: 'Navbar',

    methods: {
        logout() {
            localStorage.removeItem('access')
            localStorage.removeItem('refresh')

            router.replace('/')
        }
    }
}
</script>
