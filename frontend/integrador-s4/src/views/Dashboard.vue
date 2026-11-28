<template>
    <div class="min-h-screen bg-gray-50">

        <Navbar />

        <main class="px-6 py-5 md:px-12">

            <!-- Cabeçalho -->
            <div class="mb-10 flex flex-col md:flex-row md:items-center md:justify-between gap-4">

                <div>
                    <h1 class="text-3xl font-bold">
                        Dashboard
                    </h1>
                </div>

                <button
                    @click="carregarAtivos"
                    :disabled="loading"
                    class="px-5 py-3 rounded-lg border border-[#8fcf8f]
                           text-gray-700 font-semibold
                           hover:bg-[#E5F8EC] transition
                           disabled:opacity-50 cursor-pointer"
                >
                    {{ loading ? 'Atualizando...' : 'Atualizar dados' }}
                </button>

            </div>

            <!-- Carregamento -->
            <div
                v-if="loading"
                class="bg-white rounded-xl border border-gray-200 p-8 text-center mb-8"
            >
                <p class="text-gray-500">
                    Carregando informações dos ativos...
                </p>
            </div>

            <!-- Erro -->
            <div
                v-else-if="error"
                class="bg-red-50 border border-red-200 rounded-xl p-5 mb-8"
            >
                <p class="text-red-700">
                    {{ error }}
                </p>

                <button
                    @click="carregarAtivos"
                    class="mt-3 text-red-700 underline font-semibold cursor-pointer"
                >
                    Tentar novamente
                </button>
            </div>

            <template v-else>

                <!-- Indicadores -->
                <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">

                    <div
                        v-for="status in statusCards"
                        :key="status.id"
                        class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm"
                    >

                        <div class="flex items-center justify-between">

                            <span class="text-gray-500 text-sm">
                                {{ status.label }}
                            </span>

                            <span
                                class="w-3 h-3 rounded-full"
                                :style="{ backgroundColor: status.color }"
                            ></span>

                        </div>

                        <div class="mt-4 flex items-end gap-2">

                            <span class="text-4xl font-bold text-gray-800">
                                {{ status.quantity }}
                            </span>

                            <span class="text-sm text-gray-400 mb-1">
                                computadores
                            </span>

                        </div>

                    </div>

                </section>

                <!-- Gráficos -->
                <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">

                    <!-- Gráfico de rosca -->
                    <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6">

                        <h2 class="text-lg font-semibold text-gray-800">
                            Distribuição das máquinas
                        </h2>

                        <div class="flex flex-col items-center justify-center py-8">

                            <div
                                class="relative w-56 h-56 rounded-full"
                                :style="{ background: donutGradient }"
                            >

                                <div
                                    class="absolute inset-5 bg-white rounded-full
                                           flex flex-col items-center justify-center"
                                >

                                    <span class="text-4xl font-bold text-gray-800">
                                        {{ totalMachines }}
                                    </span>

                                    <span class="text-sm text-gray-400">
                                        Total de máquinas
                                    </span>

                                </div>

                            </div>

                            <!-- Legenda -->
                            <div class="grid grid-cols-1 sm:grid-cols-3 gap-5 mt-8 w-full">

                                <div
                                    v-for="status in statusCards"
                                    :key="status.id"
                                    class="flex items-center gap-2"
                                >

                                    <span
                                        class="w-3 h-3 rounded-full shrink-0"
                                        :style="{ backgroundColor: status.color }"
                                    ></span>

                                    <div>

                                        <p class="text-sm text-gray-500">
                                            {{ status.label }}
                                        </p>

                                        <p class="text-lg font-semibold text-gray-800">
                                            {{ percentage(status.quantity) }}%
                                        </p>

                                    </div>

                                </div>

                            </div>

                        </div>

                    </div>

                    <!-- Gráfico de barras -->
                    <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6">

                        <h2 class="text-lg font-semibold text-gray-800">
                            Máquinas por situação
                        </h2>

                        <div class="flex flex-col gap-9 py-10">

                            <div
                                v-for="status in statusCards"
                                :key="status.id"
                            >

                                <div class="flex justify-between mb-3">

                                    <span class="text-sm text-gray-600">
                                        {{ status.label }}
                                    </span>

                                    <span class="text-sm font-semibold text-gray-800">
                                        {{ status.quantity }}
                                    </span>

                                </div>

                                <div class="w-full h-4 bg-gray-100 rounded-full overflow-hidden">

                                    <div
                                        class="h-full rounded-full transition-all duration-500"
                                        :style="{
                                            width: percentage(status.quantity) + '%',
                                            backgroundColor: status.color
                                        }"
                                    ></div>

                                </div>

                            </div>

                        </div>

                        <div class="border-t border-gray-100 pt-5 mt-4">

                            <div class="flex justify-between text-sm text-gray-500">

                                <span>
                                    Total de computadores
                                </span>

                                <span class="font-semibold text-gray-800">
                                    {{ totalMachines }}
                                </span>

                            </div>

                        </div>

                    </div>

                </section>

            </template>

        </main>

    </div>
</template>


<script>
import Navbar from '../components/navbarVue.vue'

export default {

    name: 'Dashboard',

    components: {
        Navbar
    },

    data() {
        return {

            machines: [],

            loading: true,

            error: null,

            apiUrl: `${import.meta.env.VITE_API_URL}/api/ativo`

        }
    },

    computed: {

        // Quantidade total de computadores
        totalMachines() {
            return this.machines.length
        },

        // Quantidade de computadores por situação
        statusCards() {

            const statuses = [

                {
                    id: 'DISPONIVEL',
                    label: 'Disponíveis',
                    color: '#22C55E'
                },

                {
                    id: 'MANUTENCAO',
                    label: 'Em manutenção',
                    color: '#F59E0B'
                },

                {
                    id: 'INDISPONIVEL',
                    label: 'Indisponíveis',
                    color: '#EF4444'
                }

            ]

            return statuses.map(status => ({

                ...status,

                quantity: this.machines.filter(machine =>
                    machine.status === status.id
                ).length

            }))

        },

        // Geração dinâmica do gráfico de rosca
        donutGradient() {

            if (this.totalMachines === 0) {
                return '#E5E7EB'
            }

            let currentPercentage = 0

            const segments = this.statusCards.map(status => {

                const start = currentPercentage

                const percentage =
                    (status.quantity / this.totalMachines) * 100

                currentPercentage += percentage

                return `${status.color} ${start}% ${currentPercentage}%`

            })

            return `conic-gradient(${segments.join(', ')})`

        }

    },

    methods: {

        // Consulta os ativos na API Django
        async carregarAtivos() {
            this.loading = true
            this.error = null

            try {
                const token = localStorage.getItem('access')

                if (!token) {
                    throw new Error('Sessão não encontrada. Faça login novamente.')
                }

                const response = await fetch(this.apiUrl, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                })

                if (response.status === 401) {
                    throw new Error('Sessão expirada. Faça login novamente.')
                }

                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`)
                }

                const data = await response.json()

                const ativos = Array.isArray(data)
                    ? data
                    : data.results || data.data || []

                this.machines = ativos.map(ativo => ({
                    id: ativo.id,
                    name: ativo.nome,
                    patrimonio: ativo.patrimonio,
                    status: String(ativo.status || '').trim().toUpperCase(),
                    laboratorio: ativo.laboratorio,
                    categoria: ativo.categoria
                }))

            } catch (error) {
                console.error('Erro ao carregar ativos:', error)

                this.error = error.message ||
                    'Não foi possível carregar os ativos. Verifique a conexão com o servidor.'

            } finally {
                this.loading = false
            }
        },

        // Calcula a porcentagem de cada situação
        percentage(quantity) {

            if (this.totalMachines === 0) {
                return 0
            }

            return Math.round(
                (quantity / this.totalMachines) * 100
            )

        }

    },

    // Carrega os dados ao abrir a Dashboard
    mounted() {

        this.carregarAtivos()

    }

}
</script>