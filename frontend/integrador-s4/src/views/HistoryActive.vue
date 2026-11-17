
<template>
    <Navbar />

    <div class="min-h-screen bg-gray-50">
        <main class="px-6 py-10 md:px-12">

            <!-- Cabeçalho -->
            <div class="mb-8">
                <h1 class="text-3xl font-bold text-center">
                    Histórico de movimentações
                </h1>
            </div>

            <!-- Filtros -->
            <section class="bg-white p-5 rounded-xl border border-gray-200 mb-6">

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
                            :max="endDate || undefined"
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
            </section>

            <!-- Tabela -->
            <section class="bg-white rounded-xl border border-gray-200 shadow-sm">

                <div class="p-5 border-b border-gray-200 flex justify-between items-center flex-wrap gap-3">

                    <div>
                        <h2 class="text-lg font-semibold text-gray-800">
                            Registros de movimentação
                        </h2>

                        <p class="text-sm text-gray-400 mt-1">
                            {{ filteredHistory.length }} registros encontrados
                        </p>
                    </div>

                    <button
                        @click="fetchHistory"
                        :disabled="loading"
                        class="px-4 py-2 rounded-lg bg-[#E5F8EC] text-gray-700
                               font-semibold hover:bg-[#d2f0dc] transition
                               disabled:opacity-50 cursor-pointer"
                    >
                        {{ loading ? "Atualizando..." : "Atualizar" }}
                    </button>

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

                            <!-- Carregamento -->
                            <tr v-if="loading">
                                <td colspan="6" class="text-center py-10 text-gray-400">
                                    Carregando movimentações...
                                </td>
                            </tr>

                            <!-- Erro -->
                            <tr v-else-if="error">
                                <td colspan="6" class="text-center py-10 text-red-500">
                                    {{ error }}
                                </td>
                            </tr>

                            <template v-else>

                                <!-- Registros -->
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

                                <!-- Nenhum registro -->
                                <tr v-if="filteredHistory.length === 0">
                                    <td colspan="6" class="text-center py-10 text-gray-400">
                                        Nenhuma movimentação encontrada.
                                    </td>
                                </tr>

                            </template>

                        </tbody>
                    </table>

                </div>
            </section>

        </main>
    </div>
</template>

<script>
import Navbar from "../components/navbarVue.vue";
import api from "../services/api";

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

            history: [],

            loading: false,
            error: null
        };
    },

    async mounted() {
        await this.fetchHistory();
    },

    computed: {

        // Filtrar movimentações
        filteredHistory() {

            const term = this.search.toLowerCase().trim();

            return this.history.filter(item => {

                // Pesquisa por usuário ou computador
                const matchesSearch =
                    item.user.toLowerCase().includes(term) ||
                    item.computer.toLowerCase().includes(term);

                // Data no formato ISO
                const itemDate = item.rawDate
                    ? item.rawDate.substring(0, 10)
                    : "";

                // Data inicial
                const matchesStartDate =
                    !this.startDate ||
                    itemDate >= this.startDate;

                // Data final
                const matchesEndDate =
                    !this.endDate ||
                    itemDate <= this.endDate;

                return (
                    matchesSearch &&
                    matchesStartDate &&
                    matchesEndDate
                );
            });
        }
    },

    methods: {

        // Buscar movimentações na API
        
        async fetchHistory() {

            this.loading = true;
            this.error = null;

            try {

                const response = await api.get("movimentacao/");

                const data = response.data;

                const records = Array.isArray(data)
                    ? data
                    : data.results ?? [];

                this.history = records.map(item => {

                    const usuario = item.usuario_detalhes;
                    const ativo = item.ativo_detalhes;

                    const origem = item.laboratorio_origem;
                    const destino = item.laboratorio_destino;

                    // Identificação do usuário
                    const user = usuario
                        ? [
                            usuario.first_name,
                            usuario.last_name
                        ].filter(Boolean).join(" ") ||
                        usuario.email ||
                        "Usuário não identificado"
                        : "Usuário não identificado";

                    // Separação do patrimônio e nome do computador
                    const patrimonio = ativo?.patrimonio ||
                                    ativo?.numero_patrimonio ||
                                    "";

                    const nomeComputador = ativo?.nome || "";

                    const computer = patrimonio && nomeComputador
                        ? `${patrimonio} - ${nomeComputador}`
                        : patrimonio || nomeComputador || "Ativo não identificado";

                    // Nome dos laboratórios
                    const salaOrigem = origem || "-";
                    const salaDestino = destino || "-";

                    // Situação do ativo
                    const status = ativo?.status ||
                                ativo?.situacao ||
                                "-";

                    // Data da movimentação
                    const rawDate = item.data_movimentacao || "";

                    return {
                        id: item.id,
                        user,
                        computer,
                        origin: salaOrigem,
                        destination: salaDestino,
                        status,
                        rawDate,
                        date: this.formatDate(rawDate)
                    };

                });

                console.log("Movimentações recebidas:", this.history);

            } catch (error) {

                console.error("Erro ao buscar movimentações:", error);

                this.error =
                    "Não foi possível carregar o histórico de movimentações.";

            } finally {

                this.loading = false;

            }
        },

        // Formatar data e horário
        formatDate(date) {

            if (!date) {
                return "-";
            }

            const parsedDate = new Date(date);

            if (isNaN(parsedDate.getTime())) {
                return "-";
            }

            return parsedDate.toLocaleString("pt-BR", {
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit"
            });
        },

        // Cores da situação
        statusClass(status) {

            const classes = {
                "DISPONIVEL": "bg-green-100 text-green-700",
                "MANUTENÇÃO": "bg-blue-100 text-blue-700",
                "INDISPONÍVEL": "bg-red-100 text-red-700"
            };

            return classes[status] || "bg-gray-100 text-gray-600";
        },

        // Limpar filtros
        clearFilters() {

            this.search = "";
            this.startDate = "";
            this.endDate = "";

        }
    }
};
</script>
