
<template>
    <Navbar />

    <div class="min-h-[calc(100dvh-80px)] bg-gray-50">
        <main class="px-6 py-10 md:px-12">

            <!-- Cabeçalho -->
            <div class="mb-8">
                <h1 class="text-3xl font-bold text-center text-gray-800">
                    Ativos
                </h1>
            </div>

            <!-- Filtros -->
            <section class="bg-white p-5 rounded-xl border border-gray-200 mb-6">

                <!-- Pesquisa -->
                <div class="mb-5">
                    <label class="block text-sm font-semibold text-gray-700 mb-2">
                        Pesquisar ativos
                    </label>

                    <input
                        v-model="search"
                        type="text"
                        placeholder="Digite o patrimônio, nome, descrição ou categoria..."
                        class="w-full border border-gray-300 rounded-lg px-4 py-3
                               outline-none focus:border-[#8fcf8f] transition"
                    />
                </div>

                <!-- Filtros de status -->
                <div>
                    <div class="flex flex-wrap gap-3">

                        <button
                            @click="selectedStatus = ''"
                            :class="selectedStatus === ''
                                ? 'bg-[#E5F8EC] border-[#8fcf8f] text-gray-800'
                                : 'bg-white border-gray-300 text-gray-600'"
                            class="px-5 py-2.5 rounded-lg border font-semibold
                                   hover:bg-[#E5F8EC] transition cursor-pointer"
                        >
                            Todos
                        </button>

                        <button
                            @click="selectedStatus = 'DISPONIVEL'"
                            :class="selectedStatus === 'DISPONIVEL'
                                ? 'bg-[#E5F8EC] border-[#8fcf8f] text-gray-800'
                                : 'bg-white border-gray-300 text-gray-600'"
                            class="px-5 py-2.5 rounded-lg border font-semibold
                                   hover:bg-[#E5F8EC] transition cursor-pointer"
                        >
                            Disponível
                        </button>

                        <button
                            @click="selectedStatus = 'INDISPONIVEL'"
                            :class="selectedStatus === 'INDISPONIVEL'
                                ? 'bg-[#E5F8EC] border-[#8fcf8f] text-gray-800'
                                : 'bg-white border-gray-300 text-gray-600'"
                            class="px-5 py-2.5 rounded-lg border font-semibold
                                   hover:bg-[#E5F8EC] transition cursor-pointer"
                        >
                            Indisponível
                        </button>

                        <button
                            @click="selectedStatus = 'MANUTENCAO'"
                            :class="selectedStatus === 'MANUTENCAO'
                                ? 'bg-[#E5F8EC] border-[#8fcf8f] text-gray-800'
                                : 'bg-white border-gray-300 text-gray-600'"
                            class="px-5 py-2.5 rounded-lg border font-semibold
                                   hover:bg-[#E5F8EC] transition cursor-pointer"
                        >
                            Manutenção
                        </button>

                        <button
                            @click="clearFilters"
                            class="ml-auto px-5 py-2.5 rounded-lg border font-semibold
                                   hover:bg-[#E5F8EC] transition cursor-pointer"
                        >
                            Limpar filtros
                        </button>

                    </div>
                </div>

            </section>

            <!-- Tabela -->
            <section class="bg-white rounded-xl border border-gray-200 shadow-sm">

                <!-- Cabeçalho da tabela -->
                <div class="p-5 border-b border-gray-200 flex justify-between
                            items-center flex-wrap gap-3">

                    <div>
                        <h2 class="text-lg font-semibold text-gray-800">
                            Cadastro de ativos
                        </h2>

                        <p class="text-sm text-gray-400 mt-1">
                            {{ filteredAssets.length }}
                            {{ filteredAssets.length === 1 ? 'ativo encontrado' : 'ativos encontrados' }}
                        </p>
                    </div>

                    <button
                        @click="fetchAssets"
                        :disabled="loading"
                        class="px-4 py-2 rounded-lg bg-[#E5F8EC] text-gray-700
                               font-semibold hover:bg-[#d2f0dc] transition
                               disabled:opacity-50 cursor-pointer"
                    >
                        {{ loading ? "Atualizando..." : "Atualizar" }}
                    </button>

                </div>

                <!-- Conteúdo da tabela -->
                <div class="overflow-x-auto">

                    <table class="w-full text-left border-collapse">

                        <thead class="bg-gray-50">
                            <tr class="text-gray-500 text-sm">

                                <th class="px-6 py-4 font-semibold">
                                    Patrimônio
                                </th>

                                <th class="px-6 py-4 font-semibold">
                                    Nome
                                </th>

                                <th class="px-6 py-4 font-semibold">
                                    Descrição
                                </th>

                                <th class="px-6 py-4 font-semibold">
                                    Status
                                </th>

                                <th class="px-6 py-4 font-semibold">
                                    Categoria
                                </th>

                                <th class="px-6 py-4 font-semibold">
                                    Laboratório
                                </th>

                            </tr>
                        </thead>

                        <tbody>

                            <!-- Carregamento -->
                            <tr v-if="loading">
                                <td colspan="6"
                                    class="text-center py-10 text-gray-400">
                                    Carregando ativos...
                                </td>
                            </tr>

                            <!-- Erro -->
                            <tr v-else-if="error">
                                <td colspan="6"
                                    class="text-center py-10 text-red-500">
                                    {{ error }}
                                </td>
                            </tr>

                            <template v-else>

                                <!-- Registros -->
                                <tr
                                    v-for="item in filteredAssets"
                                    :key="item.id"
                                    @click="openAsset(item)"
                                    @keydown.enter="openAsset(item)"
                                    tabindex="0"
                                    role="link"
                                    :aria-label="`Ver detalhes do ativo ${item.nome}`"
                                    class="border-t border-gray-100 hover:bg-[#E5F8EC]
                                           transition cursor-pointer
                                           focus:outline-none focus:bg-[#E5F8EC]"
                                >

                                    <!-- Patrimônio -->
                                    <td class="px-6 py-5 font-semibold text-gray-800 whitespace-nowrap">
                                        {{ item.patrimonio }}
                                    </td>

                                    <!-- Nome -->
                                    <td class="px-6 py-5 text-gray-700 whitespace-nowrap">
                                        {{ item.nome }}
                                    </td>

                                    <!-- Descrição -->
                                    <td class="px-6 py-5 text-gray-600 min-w-[220px]">
                                        {{ item.descricao || '-' }}
                                    </td>

                                    <!-- Status editável -->
                                    <td class="px-6 py-5 whitespace-nowrap">

                                        <select
                                            :value="item.status"
                                            @click.stop
                                            @keydown.stop
                                            @change="updateStatus(item, $event.target.value)"
                                            :disabled="updatingIds.includes(item.id)"
                                            class="px-3 py-2 rounded-lg text-xs font-semibold
                                                   border border-gray-200 outline-none
                                                   cursor-pointer
                                                   bg-gray-100 text-gray-700
                                                   hover:bg-[#E5F8EC]
                                                   hover:border-[#8fcf8f]
                                                   transition duration-200
                                                   disabled:opacity-50
                                                   disabled:cursor-wait"
                                        >
                                            <option value="INDISPONIVEL">
                                                Indisponível
                                            </option>

                                            <option value="DISPONIVEL">
                                                Disponível
                                            </option>

                                            <option value="MANUTENCAO">
                                                Manutenção
                                            </option>
                                        </select>

                                        <span
                                            v-if="updatingIds.includes(item.id)"
                                            class="ml-2 text-xs text-gray-400"
                                        >
                                            Salvando...
                                        </span>

                                    </td>

                                    <!-- Categoria -->
                                    <td class="px-6 py-5 text-gray-600 whitespace-nowrap">
                                        {{ item.categoriaNome }}
                                    </td>

                                    <!-- Laboratório -->
                                    <td class="px-6 py-5 text-gray-600 whitespace-nowrap">
                                        {{ item.laboratorioNome }}
                                    </td>

                                </tr>

                                <!-- Nenhum registro -->
                                <tr v-if="filteredAssets.length === 0">
                                    <td colspan="6"
                                        class="text-center py-10 text-gray-400">
                                        Nenhum ativo encontrado.
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
    name: "Ativos",

    components: {
        Navbar
    },

    data() {
        return {
            search: "",
            selectedStatus: "",

            assets: [],

            loading: false,
            error: null,

            updatingIds: []
        };
    },

    async mounted() {
        await this.fetchAssets();
    },

    computed: {

        // Filtragem dos ativos
        filteredAssets() {

            const term = this.search.toLowerCase().trim();

            return this.assets.filter(item => {

                // Pesquisa textual
                const matchesSearch =
                    String(item.patrimonio || "").toLowerCase().includes(term) ||
                    String(item.nome || "").toLowerCase().includes(term) ||
                    String(item.descricao || "").toLowerCase().includes(term) ||
                    String(item.categoriaNome || "").toLowerCase().includes(term) ||
                    String(item.laboratorioNome || "").toLowerCase().includes(term);

                // Filtro de status
                const matchesStatus =
                    !this.selectedStatus ||
                    item.status === this.selectedStatus;

                return matchesSearch && matchesStatus;
            });
        }
    },

    methods: {

        // Abrir detalhes do ativo
        openAsset(item) {
            this.$router.push({
                name: "AtivoDetalhes",
                params: {
                    id: item.id
                }
            });
        },

        // Buscar ativos na API
        async fetchAssets() {

            this.loading = true;
            this.error = null;

            try {

                const response = await api.get("ativo/");

                const data = response.data;

                const records = Array.isArray(data)
                    ? data
                    : data.results ?? [];

                this.assets = records.map(item => {

                    // Categoria
                    const categoria = item.categoria_detalhes ?? item.categoria;

                    let categoriaNome = "-";

                    if (categoria && typeof categoria === "object") {
                        categoriaNome =
                            categoria.nome ||
                            categoria.name ||
                            categoria.titulo ||
                            categoria.descricao ||
                            "-";
                    } else if (categoria !== null && categoria !== undefined) {
                        categoriaNome = `Categoria #${categoria}`;
                    }

                    // Laboratório
                    const laboratorio = item.laboratorio_detalhes ?? item.laboratorio;

                    let laboratorioNome = "-";

                    if (laboratorio && typeof laboratorio === "object") {
                        laboratorioNome =
                            laboratorio.nome ||
                            laboratorio.name ||
                            laboratorio.titulo ||
                            "-";
                    } else if (laboratorio !== null && laboratorio !== undefined) {
                        laboratorioNome = `Laboratório #${laboratorio}`;
                    }

                    return {
                        id: item.id,
                        patrimonio: item.patrimonio || "-",
                        nome: item.nome || "-",
                        descricao: item.descricao || "-",
                        status: item.status,
                        categoriaNome,
                        laboratorioNome
                    };

                });

            } catch (error) {

                console.error("Erro ao buscar ativos:", error);

                this.error =
                    "Não foi possível carregar os ativos. Tente novamente.";

            } finally {

                this.loading = false;

            }
        },

        // Atualizar status do ativo
        async updateStatus(item, newStatus) {

            const previousStatus = item.status;

            if (previousStatus === newStatus) {
                return;
            }

            if (this.updatingIds.includes(item.id)) {
                return;
            }

            this.updatingIds.push(item.id);

            try {

                await api.patch(`ativo/${item.id}/`, {
                    status: newStatus
                });

                // Atualiza a interface somente após a confirmação da API
                item.status = newStatus;

            } catch (error) {

                console.error("Erro ao atualizar status:", error);

                alert(
                    "Não foi possível atualizar o status do ativo. Verifique a API e tente novamente."
                );

            } finally {

                this.updatingIds = this.updatingIds.filter(
                    id => id !== item.id
                );

            }
        },

        // Classes visuais dos status
        statusClass(status) {

            const classes = {
                "DISPONIVEL": "bg-green-100 text-green-700",
                "INDISPONIVEL": "bg-red-100 text-red-700",
                "MANUTENCAO": "bg-blue-100 text-blue-700"
            };

            return classes[status] || "bg-gray-100 text-gray-600";
        },

        // Limpar filtros
        clearFilters() {

            this.search = "";
            this.selectedStatus = "";

        }
    }
};
</script>
