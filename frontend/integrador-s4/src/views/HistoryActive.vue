<template>
    <Navbar/>
    <div class="min-h-screen bg-gray-50">

        <main class="px-6 py-10 md:px-12">

            <!-- Cabeçalho -->
            <div class="mb-8">
                <h1 class="text-3xl font-bold text-center">
                    Histórico de movimentações
                </h1>
            </div>

            <div class="bg-white p-5 rounded-xl border border-gray-200 mb-6">

                <div class="mb-5">
                    <label class="block text-sm font-semibold text-gray-700 mb-2">
                        Pesquisar movimentações
                    </label>

                    <input
                        v-model="search"
                        type="text"
                        placeholder="Digite o usuário ou número do computador..."
                        class="w-full border border-gray-300 rounded-lg px-4 py-3
                            outline-none focus:border-[#8fcf8f] transition"
                    />
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            Data inicial
                        </label>

                        <input
                            v-model="startDate"
                            type="date"
                            class="w-full border border-gray-300 rounded-lg px-4 py-3
                                outline-none focus:border-[#8fcf8f] transition"
                        />
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            Data final
                        </label>

                        <input
                            v-model="endDate"
                            type="date"
                            :min="startDate || undefined"
                            class="w-full border border-gray-300 rounded-lg px-4 py-3
                                outline-none focus:border-[#8fcf8f] transition"
                        />
                    </div>

                    <div class="flex items-end">
                        <button
                            @click="clearFilters"
                            class="w-full py-3 rounded-lg border border-[#8fcf8f]
                                text-gray-700 font-semibold
                                hover:bg-[#E5F8EC] transition cursor-pointer"
                        >
                            Limpar filtros
                        </button>
                    </div>

                </div>

            </div>

            <!-- Tabela -->
            <div class="bg-white rounded-xl border border-gray-200 shadow-sm">

                <div class="p-5 border-b border-gray-200">
                    <h2 class="text-lg font-semibold text-gray-800">
                        Registros de movimentação
                    </h2>

                    <p class="text-sm text-gray-400 mt-1">
                        {{ filteredHistory.length }} registros encontrados
                    </p>
                </div>

                <div class="overflow-x-auto">

                    <table class="w-full text-left border-collapse">

                        <thead class="bg-gray-50">
                            <tr class="text-gray-500 text-sm">

                                <th class="px-6 py-4 font-semibold">
                                    Usuário
                                </th>

                                <th class="px-6 py-4 font-semibold">
                                    Computador
                                </th>

                                <th class="px-6 py-4 font-semibold">
                                    Sala de origem
                                </th>

                                <th class="px-6 py-4 font-semibold">
                                    Sala de destino
                                </th>

                                <th class="px-6 py-4 font-semibold">
                                    Situação
                                </th>

                                <th class="px-6 py-4 font-semibold">
                                    Data / Hora
                                </th>

                            </tr>
                        </thead>

                        <tbody>

                            <tr
                                v-for="item in filteredHistory"
                                :key="item.id"
                                class="border-t border-gray-100 hover:bg-gray-50 transition"
                            >

                                <td class="px-6 py-5 text-gray-700 whitespace-nowrap">
                                    {{ item.user }}
                                </td>

                                <td class="px-6 py-5 font-semibold text-gray-800 whitespace-nowrap">
                                    {{ item.computer }}
                                </td>

                                <td class="px-6 py-5 text-gray-600 whitespace-nowrap">
                                    {{ item.origin }}
                                </td>

                                <td class="px-6 py-5 text-gray-600 whitespace-nowrap">
                                    {{ item.destination }}
                                </td>

                                <td class="px-6 py-5 whitespace-nowrap">

                                    <span
                                        class="px-3 py-1 rounded-full text-xs font-semibold"
                                        :class="statusClass(item.status)"
                                    >
                                        {{ item.status }}
                                    </span>

                                </td>

                                <td class="px-6 py-5 text-gray-500 text-sm whitespace-nowrap">
                                    {{ item.date }}
                                </td>

                            </tr>

                            <tr v-if="filteredHistory.length === 0">
                                <td
                                    colspan="6"
                                    class="text-center py-10 text-gray-400"
                                >
                                    Nenhuma movimentação encontrada.
                                </td>
                            </tr>

                        </tbody>

                    </table>

                </div>
            </div>

        </main>
    </div>
</template>

<script>
import Navbar from "../components/navbarVue.vue"
export default {
    name: "HistoryActive",
    components: {
        Navbar
    },
    
    data() {
        return {
            search: "",
            startDate: "",
            endDate: "",

            // Dados fictícios para demonstração.
            history: [
                {
                    id: 1,
                    user: "Igor Matheus",
                    computer: "PC-001",
                    origin: "Sala 01",
                    destination: "Sala 03",
                    status: "Operando",
                    date: "04/11/2026 09:30"
                },
                {
                    id: 2,
                    user: "Danilo Macri",
                    computer: "PC-002",
                    origin: "Sala 02",
                    destination: "Sala 02",
                    status: "Manutenção",
                    date: "04/11/2026 10:15"
                },
                {
                    id: 3,
                    user: "Danilo Nunes",
                    computer: "PC-003",
                    origin: "Sala 04",
                    destination: "Sala 01",
                    status: "Operando",
                    date: "04/11/2026 11:20"
                },
                {
                    id: 4,
                    user: "Igor Matheus",
                    computer: "PC-004",
                    origin: "Sala 03",
                    destination: "Sala 03",
                    status: "Desativado",
                    date: "04/11/2026 13:45"
                },
                {
                    id: 5,
                    user: "Danilo Macri",
                    computer: "PC-005",
                    origin: "Sala 01",
                    destination: "Sala 02",
                    status: "Operando",
                    date: "04/11/2026 14:10"
                }
            ]
        }
    },

    computed: {
        filteredHistory() {
            const term = this.search.toLowerCase()

            return this.history.filter(item => {

                // Filtro por usuário ou computador
                const matchesSearch =
                    item.user.toLowerCase().includes(term) ||
                    item.computer.toLowerCase().includes(term)

                // Conversão da data brasileira para formato ISO
                const [datePart] = item.date.split(" ")
                const [day, month, year] = datePart.split("/")

                const itemDate = `${year}-${month}-${day}`

                // Filtro por período
                const matchesStartDate =
                    !this.startDate || itemDate >= this.startDate

                const matchesEndDate =
                    !this.endDate || itemDate <= this.endDate

                return (
                    matchesSearch &&
                    matchesStartDate &&
                    matchesEndDate
                )
            })
        }
    },

    methods: {
        statusClass(status) {
            const classes = {
                "Operando": "bg-green-100 text-green-700",
                "Manutenção": "bg-yellow-100 text-yellow-700",
                "Desativado": "bg-red-100 text-red-700"
            }

            return classes[status]
        },
        clearFilters() {
            this.search = ""
            this.startDate = ""
            this.endDate = ""
        }
    }
}
</script>
