
<template>
    <section>
        <nav
            class="sticky top-0 z-[999] w-full bg-[#8fcf8f] shadow-[0_5px_15px_rgba(0,0,0,0.25)]"
        >
            <div
                class="mx-auto flex min-h-[80px] w-full max-w-[1600px] items-center justify-between px-10 max-[600px]:px-4 max-[1023px]:px-6"
            >
                <!-- LOGO -->
                <router-link
                    to="/home"
                    class="flex shrink-0 items-center no-underline"
                    @click="fecharMenu"
                >
                    <img
                        src="/logo-tracklog-minimalist.png"
                        alt="Logo Tracklog"
                        class="block h-auto max-h-[65px] w-[150px] object-contain"
                    />
                </router-link>

                <!-- MENU DESKTOP -->
                <ul
                    class="m-0 hidden list-none items-center gap-[15px] p-0 lg:flex"
                >
                    <li v-for="item in menuItems" :key="item.to">
                        <router-link
                            :to="item.to"
                            class="block whitespace-nowrap rounded-[20px] px-[18px] py-[10px] text-[18px] font-medium text-[#155b38] no-underline transition-all duration-300 hover:bg-[#a1e7a0] hover:text-[#155b38]"
                        >
                            {{ item.nome }}
                        </router-link>
                    </li>

                    <!-- LOGOUT DESKTOP -->
                    <li>
                        <button
                            type="button"
                            @click="logout"
                            class="flex cursor-pointer items-center justify-center gap-2 whitespace-nowrap rounded-[20px] border-none bg-[#155b38] px-[18px] py-[10px] text-[17px] font-semibold text-white transition-all duration-300 hover:-translate-y-0.5 hover:bg-[#a32929]"
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

                <!-- BOTÃO MENU MOBILE -->
                <button
                    type="button"
                    @click="menuAberto = !menuAberto"
                    :aria-expanded="menuAberto"
                    aria-label="Abrir ou fechar menu"
                    class="flex h-11 w-11 cursor-pointer items-center justify-center rounded-xl border-none bg-[#155b38] text-white transition hover:bg-[#12482e] lg:hidden"
                >
                    <!-- ÍCONE MENU -->
                    <svg
                        v-if="!menuAberto"
                        xmlns="http://www.w3.org/2000/svg"
                        width="26"
                        height="26"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                    >
                        <line x1="3" y1="6" x2="21" y2="6" />
                        <line x1="3" y1="12" x2="21" y2="12" />
                        <line x1="3" y1="18" x2="21" y2="18" />
                    </svg>

                    <!-- ÍCONE FECHAR -->
                    <svg
                        v-else
                        xmlns="http://www.w3.org/2000/svg"
                        width="26"
                        height="26"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                    >
                        <line x1="18" y1="6" x2="6" y2="18" />
                        <line x1="6" y1="6" x2="18" y2="18" />
                    </svg>
                </button>
            </div>

            <!-- MENU MOBILE -->
            <div
                v-if="menuAberto"
                class="border-t border-[#70b970] bg-[#8fcf8f] px-4 pb-5 pt-3 lg:hidden"
            >
                <ul class="mx-auto flex max-w-[600px] list-none flex-col gap-2 p-0">
                    <li v-for="item in menuItems" :key="item.to">
                        <router-link
                            :to="item.to"
                            @click="fecharMenu"
                            class="block rounded-xl px-5 py-3 text-center text-lg font-medium text-[#155b38] no-underline transition-all duration-300 hover:bg-[#a1e7a0]"
                        >
                            {{ item.nome }}
                        </router-link>
                    </li>

                    <!-- LOGOUT MOBILE -->
                    <li class="pt-2">
                        <button
                            type="button"
                            @click="logout"
                            class="flex w-full cursor-pointer items-center justify-center gap-2 rounded-xl border-none bg-[#155b38] px-5 py-3 text-lg font-semibold text-white transition-all duration-300 hover:bg-[#a32929]"
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

    data() {
        return {
            menuAberto: false,

            menuItems: [
                { nome: 'Home', to: '/home' },
                { nome: 'Ativos', to: '/ativos' },
                { nome: 'Dashboard', to: '/dashboard' },
                { nome: 'Histórico', to: '/historico' },
                { nome: 'Serviços', to: '/servicos' }
            ]
        }
    },

    methods: {
        fecharMenu() {
            this.menuAberto = false
        },

        logout() {
            localStorage.removeItem('access')
            localStorage.removeItem('refresh')

            this.fecharMenu()

            router.replace('/')
        }
    }
}
</script>
