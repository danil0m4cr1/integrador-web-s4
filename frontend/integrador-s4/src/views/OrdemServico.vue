
<template>
    <Navbar />

    <main class="min-h-[calc(100dvh-80px)] bg-gray-50 px-4 pt-3 pb-4 sm:px-5 md:px-8 lg:px-12">
        <!-- CABEÇALHO -->
        <section class="mx-auto mb-4 mt-3 grid max-w-7xl grid-cols-1 items-center gap-4 lg:grid-cols-[1fr_auto_1fr]">
            <div class="text-center lg:col-start-2 lg:row-start-1">
                <h1 class="text-2xl font-bold text-gray-800 md:text-3xl">
                    Ordens de Serviço
                </h1>
            </div>

            <div class="flex w-full items-center justify-end gap-2 lg:col-start-3 lg:row-start-1">
                <button
                    @click="abrirFormulario"
                    aria-label="Adicionar ordem"
                    title="Adicionar ordem"
                    class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-green-600 text-2xl font-semibold
                     text-white shadow-sm transition hover:bg-green-700 cursor-pointer"
                >
                    +
                </button>

                <button
                    @click="removerOrdem"
                    :disabled="ordensFiltradas.length === 0"
                    aria-label="Remover ordem"
                    title="Remover ordem"
                    class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-600 text-2xl
                     font-semibold text-white shadow-sm transition hover:bg-red-700 disabled:cursor-not-allowed 
                     disabled:opacity-40 cursor-pointer"
                >
                    −
                </button>

                <div class="rounded-xl border border-gray-200 bg-white px-4 py-2 shadow-sm">
                    <p class="text-center text-xs text-gray-500">Exibidas</p>
                    <p class="text-center text-lg font-bold text-gray-800">
                        {{ ordensFiltradas.length }}
                    </p>
                </div>
            </div>
        </section>

        <!-- CONTEÚDO -->
        <section class="mx-auto max-w-7xl">

            <!-- FILTROS -->
            <div
                v-if="!loading && !error && ordens.length > 0"
                class="mb-5 flex flex-col items-center gap-3"
            >
                <div class="flex flex-wrap justify-center gap-2">
                    <button
                        v-for="filtro in filtrosStatus"
                        :key="filtro.valor"
                        @click="alterarFiltro(filtro.valor)"
                        class="rounded-xl border px-4 py-2 text-sm font-semibold transition cursor-pointer"
                        :class="
                            filtroStatus === filtro.valor
                                ? filtro.classeAtiva
                                : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300 hover:bg-gray-100'
                        "
                    >
                        {{ filtro.nome }}

                        <span
                            class="ml-1 rounded-full px-2 py-0.5 text-xs"
                            :class="
                                filtroStatus === filtro.valor
                                    ? 'bg-white/20'
                                    : 'bg-gray-100'
                            "
                        >
                            {{ contarOrdens(filtro.valor) }}
                        </span>
                    </button>
                </div>
            </div>

            <!-- CARREGAMENTO -->
            <div
                v-if="loading"
                class="flex min-h-[40vh] items-center justify-center"
            >
                <div class="text-center">
                    <div class="mx-auto mb-3 h-9 w-9 animate-spin rounded-full border-4 border-gray-200 border-t-green-500"></div>
                    <p class="text-sm text-gray-500">
                        Carregando ordens de serviço...
                    </p>
                </div>
            </div>

            <!-- ERRO -->
            <div
                v-else-if="error"
                class="rounded-xl border border-red-200 bg-red-50 p-5 text-center text-sm text-red-700"
            >
                {{ error }}

                <button
                    @click="buscarOrdens"
                    class="ml-2 font-semibold underline"
                >
                    Tentar novamente
                </button>
            </div>

            <!-- NENHUMA ORDEM CADASTRADA -->
            <div
                v-else-if="ordens.length === 0"
                class="flex min-h-[40vh] flex-col items-center justify-center rounded-xl border border-gray-200 bg-white p-8 text-center"
            >
                <h3 class="font-semibold text-gray-700">
                    Nenhuma ordem encontrada
                </h3>

                <p class="mt-1 text-sm text-gray-500">
                    Ainda não existem ordens de serviço cadastradas.
                </p>
            </div>

            <!-- NENHUMA ORDEM NO FILTRO -->
            <div
                v-else-if="ordensFiltradas.length === 0"
                class="flex min-h-[40vh] flex-col items-center justify-center rounded-xl border border-gray-200 bg-white p-8 text-center"
            >

                <h3 class="font-semibold text-gray-700">
                    Nenhuma ordem {{ formatarStatus(filtroStatus).toLowerCase() }}
                </h3>

                <button
                    @click="alterarFiltro('TODAS')"
                    class="mt-4 rounded-lg bg-green-600 px-4 py-2 text-sm font-semibold text-white transition 
                    hover:bg-green-700 cursor-pointer"
                >
                    Mostrar todas
                </button>
            </div>

            <!-- CARROSSEL -->
            <div
                v-else
                class="mx-auto flex w-full max-w-6xl items-center gap-2 sm:gap-3"
                :class="{ 'carrossel-unico': ordensFiltradas.length === 1 }"
            >
                <!-- SETA ESQUERDA -->
                <button
                    v-if="ordensFiltradas.length > 1"
                    @click="navegar(-1)"
                    :disabled="activeIndex === 0"
                    class="z-10 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-gray-200 bg-white text-gray-700 shadow-md transition hover:border-green-400 hover:bg-green-50 disabled:cursor-not-allowed disabled:opacity-30"
                    aria-label="Ordem anterior"
                >
                    <span class="text-2xl leading-none">‹</span>
                </button>

                <!-- ÁREA DO CARROSSEL -->
                <div
                    ref="carousel"
                    class="carousel-container flex min-w-0 flex-1 items-stretch gap-3 py-4"
                    :class="{ 'carousel-container-single': ordensFiltradas.length === 1 }"
                    @scroll.passive="atualizarCardAtivo"
                >
                    <article
                        v-for="(ordem, index) in ordensFiltradas"
                        :key="ordem.id"
                        @click="irPara(index)"
                        class="carousel-card shrink-0 cursor-pointer rounded-xl border border-gray-200 bg-white p-3 sm:p-4"
                        :class="{
                            'carousel-card-active': index === activeIndex,
                            'carousel-card-inactive': index !== activeIndex,
                            'carousel-card-single': ordensFiltradas.length === 1
                        }"
                    >
                        <!-- IDENTIFICAÇÃO -->
                        <div class="mb-3 flex items-center justify-between gap-2">
                            <span class="text-xs font-semibold uppercase tracking-wider text-gray-400">
                                Ordem #{{ ordem.id }}
                            </span>

                            <span
                                class="rounded-full px-2 py-1 text-xs font-semibold"
                                :class="statusClass(ordem.status)"
                            >
                                {{ formatarStatus(ordem.status) }}
                            </span>
                        </div>

                        <!-- ATIVO -->
                        <div class="mb-3">
                            <p class="mb-1 text-xs font-semibold uppercase tracking-wide text-gray-400">
                                Ativo em manutenção
                            </p>

                            <h3 class="break-words text-base font-bold text-gray-800 sm:text-lg">
                                {{ getAtivo(ordem).nome || "Ativo não informado" }}
                            </h3>

                            <div class="mt-1 flex flex-wrap items-center gap-2">
                                <span class="text-xs text-gray-500">
                                    Patrimônio:
                                </span>

                                <span class="rounded bg-gray-100 px-2 py-1 text-xs font-semibold text-gray-700">
                                    {{ getAtivo(ordem).patrimonio || "Não informado" }}
                                </span>
                            </div>
                        </div>

                        <!-- LABORATÓRIOS -->
                        <div class="mb-3 grid grid-cols-2 gap-2 rounded-lg bg-gray-50 p-2 sm:p-3">
                            <div class="min-w-0">
                                <p class="mb-1 text-xs font-medium text-gray-400">
                                    Origem
                                </p>

                                <p class="break-words text-xs font-semibold text-gray-700">
                                    {{ getLaboratorio(ordem, "origem") }}
                                </p>
                            </div>

                            <div class="min-w-0">
                                <p class="mb-1 text-xs font-medium text-gray-400">
                                    Destino
                                </p>

                                <p class="break-words text-xs font-semibold text-gray-700">
                                    {{ getLaboratorio(ordem, "destino") }}
                                </p>
                            </div>
                        </div>

                        <!-- DESCRIÇÃO -->
                        <div class="mb-3">
                            <p class="mb-1 text-xs font-semibold uppercase tracking-wide text-gray-400">
                                Descrição
                            </p>

                            <p class="line-clamp-2 min-h-8 break-words text-xs leading-relaxed text-gray-600">
                                {{ ordem.descricao || "Nenhuma descrição informada." }}
                            </p>
                        </div>

                        <!-- DATAS -->
                        <div class="mb-3 grid grid-cols-2 gap-2 border-y border-gray-100 py-2">
                            <div class="min-w-0">
                                <p class="text-xs text-gray-400">
                                    Data de abertura
                                </p>

                                <p class="mt-1 text-xs font-semibold text-gray-700">
                                    {{ formatarData(ordem.data_abertura) }}
                                </p>
                            </div>

                            <div class="min-w-0">
                                <p class="text-xs text-gray-400">
                                    Data de fechamento
                                </p>

                                <p class="mt-1 text-xs font-semibold text-gray-700">
                                    {{ formatarData(ordem.data_fechamento) }}
                                </p>
                            </div>
                        </div>

                        <!-- STATUS -->
                        <div @click.stop>
                            <label
                                :for="'status-' + ordem.id"
                                class="mb-1 block text-xs font-semibold text-gray-600"
                            >
                                Atualizar status da ordem
                            </label>

                            <select
                                :id="'status-' + ordem.id"
                                :value="ordem.status"
                                :disabled="atualizando === ordem.id"
                                @change="atualizarStatus(ordem, $event.target.value)"
                                class="w-full appearance-none rounded-lg border border-gray-200 bg-white px-2 py-2 text-xs text-gray-700 outline-none transition focus:border-green-400 focus:ring-2 focus:ring-green-100 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                <option value="PENDENTE">Pendente</option>
                                <option value="CONCLUIDO">Concluído</option>
                                <option value="CANCELADO">Cancelado</option>
                            </select>

                            <p
                                v-if="atualizando === ordem.id"
                                class="mt-1 text-xs text-gray-400"
                            >
                                Salvando alteração...
                            </p>
                        </div>
                    </article>
                </div>

                <!-- SETA DIREITA -->
                <button
                    v-if="ordensFiltradas.length > 1"
                    @click="navegar(1)"
                    :disabled="activeIndex === ordensFiltradas.length - 1"
                    class="z-10 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-gray-200 bg-white text-gray-700 shadow-md transition hover:border-green-400 hover:bg-green-50 disabled:cursor-not-allowed disabled:opacity-30"
                    aria-label="Próxima ordem"
                >
                    <span class="text-2xl leading-none">›</span>
                </button>
            </div>

            <!-- INDICADORES -->
            <div
                v-if="ordensFiltradas.length > 1 && !loading && !error"
                class="mt-2 flex flex-wrap justify-center gap-2"
            >
                <button
                    v-for="(ordem, index) in ordensFiltradas"
                    :key="ordem.id"
                    @click="irPara(index)"
                    :aria-label="'Ir para ordem ' + ordem.id"
                    class="h-2 rounded-full transition-all duration-300"
                    :class="
                        activeIndex === index
                            ? 'w-8 bg-green-500'
                            : 'w-2 bg-gray-300 hover:bg-green-300'
                    "
                ></button>
            </div>
        </section>
    </main>

    <!-- MODAL DE CADASTRO -->
    <Teleport to="body">
        <div
            v-if="mostrarFormulario"
            class="fixed inset-0 z-[99999] flex items-center justify-center overflow-hidden bg-black/60 p-3 sm:p-5"
            @click.self="fecharFormulario"
        >
            <section class="max-h-[calc(100dvh-2rem)] w-full max-w-xl overflow-y-auto overscroll-contain rounded-2xl bg-white p-4 shadow-2xl sm:p-6">
                <div class="mb-6 flex items-center justify-between gap-3">
                    <div>
                        <h2 class="text-xl font-bold text-gray-800">
                            Nova ordem de serviço
                        </h2>

                        <p class="mt-1 text-sm text-gray-500">
                            Preencha os dados da ordem de manutenção.
                        </p>
                    </div>

                    <button
                        @click="fecharFormulario"
                        type="button"
                        class="shrink-0 text-2xl text-gray-400 transition hover:text-gray-700"
                        aria-label="Fechar formulário"
                    >
                        &times;
                    </button>
                </div>

                <form @submit.prevent="adicionarOrdem" class="space-y-3">
                    <div>
                        <label class="mb-1 block text-sm font-semibold text-gray-700">
                            Ativo
                        </label>

                        <select
                            v-model="novaOrdem.ativo"
                            required
                            class="w-full appearance-none rounded-lg border border-gray-200 bg-white px-3 py-3 text-sm outline-none focus:border-green-500 focus:ring-2 focus:ring-green-100"
                        >
                            <option value="" disabled>
                                Selecione um ativo
                            </option>

                            <option
                                v-for="ativo in ativos"
                                :key="ativo.id"
                                :value="ativo.id"
                            >
                                {{ ativo.nome }} - Patrimônio:
                                {{ ativo.patrimonio || "Não informado" }}
                            </option>
                        </select>

                        <p
                            v-if="ativos.length === 0"
                            class="mt-1 text-xs text-red-500"
                        >
                            Nenhum ativo disponível.
                        </p>
                    </div>

                    <div>
                        <label class="mb-1 block text-sm font-semibold text-gray-700">
                            Usuário responsável
                        </label>

                        <input
                            type="text"
                            :value="usuarioEmail || 'Usuário não identificado'"
                            disabled
                            class="w-full rounded-lg border border-gray-200 bg-gray-100 px-3 py-3 text-sm text-gray-500"
                        />
                    </div>

                    <div>
                        <label class="mb-1 block text-sm font-semibold text-gray-700">
                            Descrição
                        </label>

                        <textarea
                            v-model="novaOrdem.descricao"
                            required
                            rows="3"
                            placeholder="Descreva o problema ou serviço necessário..."
                            class="w-full resize-none rounded-lg border border-gray-200 px-3 py-3 text-sm outline-none focus:border-green-500 focus:ring-2 focus:ring-green-100"
                        ></textarea>
                    </div>

                    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <div>
                            <label class="mb-1 block text-sm font-semibold text-gray-700">
                                Laboratório de origem
                            </label>

                            <select
                                v-model="novaOrdem.laboratorio_origem"
                                required
                                class="w-full appearance-none rounded-lg border border-gray-200 bg-white px-3 py-3 text-sm outline-none focus:border-green-500"
                            >
                                <option value="" disabled>
                                    Selecione
                                </option>

                                <option
                                    v-for="laboratorio in laboratorios"
                                    :key="laboratorio.id"
                                    :value="laboratorioValor(laboratorio)"
                                >
                                    {{ laboratorioNome(laboratorio) }}
                                </option>
                            </select>
                        </div>

                        <div>
                            <label class="mb-1 block text-sm font-semibold text-gray-700">
                                Laboratório de destino
                            </label>

                            <select
                                v-model="novaOrdem.laboratorio_destino"
                                required
                                class="w-full appearance-none rounded-lg border border-gray-200 bg-white px-3 py-3 text-sm outline-none focus:border-green-500"
                            >
                                <option value="" disabled>
                                    Selecione
                                </option>

                                <option
                                    v-for="laboratorio in laboratorios"
                                    :key="laboratorio.id"
                                    :value="laboratorioValor(laboratorio)"
                                >
                                    {{ laboratorioNome(laboratorio) }}
                                </option>
                            </select>
                        </div>
                    </div>

                    <div>
                        <label class="mb-1 block text-sm font-semibold text-gray-700">
                            Data de fechamento
                        </label>

                        <input
                            v-model="novaOrdem.data_fechamento"
                            type="date"
                            required
                            class="w-full rounded-lg border border-gray-200 px-3 py-3 text-sm outline-none focus:border-green-500"
                        />
                    </div>

                    <div class="flex flex-col-reverse gap-3 border-t border-gray-100 pt-5 sm:flex-row sm:justify-end">
                        <button
                            type="button"
                            @click="fecharFormulario"
                            class="rounded-lg border border-gray-200 px-5 py-2.5 text-sm font-semibold text-gray-600 transition hover:bg-gray-50"
                        >
                            Cancelar
                        </button>

                        <button
                            type="submit"
                            :disabled="salvandoOrdem || ativos.length === 0 || laboratorios.length === 0"
                            class="rounded-lg bg-green-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
                        >
                            {{ salvandoOrdem ? "Cadastrando..." : "Cadastrar ordem" }}
                        </button>
                    </div>
                </form>
            </section>
        </div>
    </Teleport>
</template>

<script>
import Navbar from "../components/navbarVue.vue";
import api from "../services/api.js";

export default {
    name: "OrdemServico",

    components: {
        Navbar
    },

    data() {
        return {
            ordens: [],
            loading: true,
            error: null,
            atualizando: null,
            activeIndex: 0,

            // Filtro atual
            filtroStatus: "TODAS",

            // Opções de filtro
            filtrosStatus: [
                {
                    nome: "Todas",
                    valor: "TODAS",
                    classeAtiva: "border-gray-700 bg-gray-800 text-white"
                },
                {
                    nome: "Pendentes",
                    valor: "PENDENTE",
                    classeAtiva: "border-yellow-500 bg-yellow-500 text-white"
                },
                {
                    nome: "Concluídas",
                    valor: "CONCLUIDO",
                    classeAtiva: "border-green-600 bg-green-600 text-white"
                },
                {
                    nome: "Canceladas",
                    valor: "CANCELADO",
                    classeAtiva: "border-red-500 bg-red-500 text-white"
                }
            ],

            mostrarFormulario: false,
            salvandoOrdem: false,

            scrollYAnterior: 0,
            estilosBodyAnteriores: null,

            ativos: [],
            laboratorios: [],

            usuarioId: localStorage.getItem("usuario_id"),
            usuarioEmail: localStorage.getItem("usuario_email"),

            novaOrdem: {
                ativo: "",
                descricao: "",
                status: "PENDENTE",
                laboratorio_origem: "",
                laboratorio_destino: "",
                data_fechamento: ""
            },

            scrollTimer: null
        };
    },

    computed: {
        // Retorna somente as ordens que correspondem ao filtro selecionado.
        ordensFiltradas() {
            if (this.filtroStatus === "TODAS") {
                return this.ordens;
            }

            return this.ordens.filter(
                ordem => ordem.status === this.filtroStatus
            );
        }
    },

    mounted() {
        this.buscarOrdens();
        window.addEventListener("resize", this.recentralizarCard);
    },

    watch: {
        mostrarFormulario(aberto) {
            if (aberto) {
                this.scrollYAnterior = window.scrollY;

                this.estilosBodyAnteriores = {
                    position: document.body.style.position,
                    top: document.body.style.top,
                    left: document.body.style.left,
                    right: document.body.style.right,
                    width: document.body.style.width,
                    overflow: document.body.style.overflow
                };

                Object.assign(document.body.style, {
                    position: "fixed",
                    top: `-${this.scrollYAnterior}px`,
                    left: "0",
                    right: "0",
                    width: "100%",
                    overflow: "hidden"
                });
            } else {
                this.restaurarScroll();
            }
        }
    },

    beforeUnmount() {
        this.restaurarScroll();
        window.removeEventListener("resize", this.recentralizarCard);

        if (this.scrollTimer) {
            clearTimeout(this.scrollTimer);
        }
    },

    methods: {
        restaurarScroll() {
            if (!this.estilosBodyAnteriores) return;

            Object.assign(document.body.style, this.estilosBodyAnteriores);

            window.scrollTo(0, this.scrollYAnterior);

            this.estilosBodyAnteriores = null;
        },

        async buscarOrdens() {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.get("ordem-servico/");

                this.ordens = Array.isArray(response.data)
                    ? response.data
                    : response.data.results || [];

                this.activeIndex = 0;

                this.$nextTick(() => {
                    if (this.ordensFiltradas.length > 0) {
                        this.centralizarCard(0, false);
                    }
                });
            } catch (error) {
                console.error("Erro ao buscar ordens:", error);

                if (error.response) {
                    this.error = `Erro ${error.response.status}: ${
                        JSON.stringify(error.response.data)
                    }`;
                } else {
                    this.error = "Não foi possível conectar ao servidor.";
                }
            } finally {
                this.loading = false;
            }
        },

        // Conta quantas ordens existem em cada status.
        contarOrdens(status) {
            if (status === "TODAS") {
                return this.ordens.length;
            }

            return this.ordens.filter(
                ordem => ordem.status === status
            ).length;
        },

        // Altera o filtro e retorna o carrossel ao primeiro card.
        alterarFiltro(status) {
            if (this.filtroStatus === status) return;

            this.filtroStatus = status;
            this.activeIndex = 0;

            this.$nextTick(() => {
                if (this.ordensFiltradas.length > 0) {
                    this.centralizarCard(0, false);
                }
            });
        },

        getAtivo(ordem) {
            if (ordem.ativo_detalhes) {
                return ordem.ativo_detalhes;
            }

            if (ordem.ativo && typeof ordem.ativo === "object") {
                return ordem.ativo;
            }

            return {};
        },

        getLaboratorio(ordem, tipo) {
            const laboratorio = tipo === "origem"
                ? ordem.laboratorio_origem
                : ordem.laboratorio_destino;

            if (laboratorio && typeof laboratorio === "object") {
                return laboratorio.nome ||
                    laboratorio.descricao ||
                    laboratorio.codigo ||
                    "Não informado";
            }

            return laboratorio || "Não informado";
        },

        async abrirFormulario() {
            this.mostrarFormulario = true;

            this.novaOrdem = {
                ativo: "",
                descricao: "",
                status: "PENDENTE",
                laboratorio_origem: "",
                laboratorio_destino: "",
                data_fechamento: ""
            };

            try {
                const [
                    responseAtivos,
                    responseLaboratorios
                ] = await Promise.all([
                    api.get("ativo/"),
                    api.get("laboratorio/")
                ]);

                this.ativos = Array.isArray(responseAtivos.data)
                    ? responseAtivos.data
                    : responseAtivos.data.results || [];

                this.laboratorios = Array.isArray(responseLaboratorios.data)
                    ? responseLaboratorios.data
                    : responseLaboratorios.data.results || [];

            } catch (error) {
                console.error("Erro ao carregar opções:", error);
                alert("Não foi possível carregar os ativos e laboratórios.");
            }
        },

        fecharFormulario() {
            if (this.salvandoOrdem) return;

            this.mostrarFormulario = false;
        },

        laboratorioValor(laboratorio) {
            return laboratorio.nome ||
                laboratorio.codigo ||
                String(laboratorio.id);
        },

        laboratorioNome(laboratorio) {
            return laboratorio.nome ||
                laboratorio.codigo ||
                `Laboratório ${laboratorio.id}`;
        },

        async adicionarOrdem() {
            const usuarioId = Number(this.usuarioId);

            if (!usuarioId) {
                alert("Não foi possível identificar o usuário. Faça login novamente.");
                return;
            }

            if (!this.novaOrdem.ativo) {
                alert("Selecione um ativo.");
                return;
            }

            if (
                this.novaOrdem.laboratorio_origem ===
                this.novaOrdem.laboratorio_destino
            ) {
                alert("O laboratório de origem e destino não podem ser iguais.");
                return;
            }

            this.salvandoOrdem = true;

            const dados = {
                ativo: Number(this.novaOrdem.ativo),
                usuario: usuarioId,
                descricao: this.novaOrdem.descricao.trim(),
                status: "PENDENTE",
                laboratorio_origem: this.novaOrdem.laboratorio_origem,
                laboratorio_destino: this.novaOrdem.laboratorio_destino,
                data_fechamento: this.novaOrdem.data_fechamento
            };

            try {
                await api.post("ordem-servico/", dados);

                this.mostrarFormulario = false;

                // A nova ordem é pendente, então seleciona esse filtro.
                this.filtroStatus = "PENDENTE";
                this.activeIndex = 0;

                await this.buscarOrdens();

                alert("Ordem de serviço cadastrada com sucesso!");
            } catch (error) {
                console.error("Erro ao cadastrar ordem:", error);

                alert(
                    error.response?.data
                        ? "Erro ao cadastrar ordem: " +
                            JSON.stringify(error.response.data)
                        : "Não foi possível conectar ao servidor."
                );
            } finally {
                this.salvandoOrdem = false;
            }
        },

        async removerOrdem() {
            const ordem = this.ordensFiltradas[this.activeIndex];

            if (!ordem) {
                alert("Nenhuma ordem selecionada.");
                return;
            }

            const confirmar = confirm(
                `Deseja realmente remover a ordem #${ordem.id}?`
            );

            if (!confirmar) return;

            try {
                await api.delete(`ordem-servico/${ordem.id}/`);

                this.ordens = this.ordens.filter(
                    item => item.id !== ordem.id
                );

                this.activeIndex = Math.max(
                    0,
                    Math.min(this.activeIndex, this.ordensFiltradas.length - 1)
                );

                this.$nextTick(() => {
                    if (this.ordensFiltradas.length > 0) {
                        this.centralizarCard(this.activeIndex, false);
                    }
                });

                alert("Ordem removida com sucesso!");
            } catch (error) {
                console.error("Erro ao remover ordem:", error);

                alert(
                    error.response?.data
                        ? JSON.stringify(error.response.data)
                        : "Não foi possível remover a ordem."
                );
            }
        },

        async atualizarStatus(ordem, novoStatus) {
            const statusAnterior = ordem.status;

            if (novoStatus === statusAnterior) return;

            this.atualizando = ordem.id;

            try {
                await api.patch(`ordem-servico/${ordem.id}/`, {
                    status: novoStatus
                });

                ordem.status = novoStatus;

                // Se a ordem deixar de pertencer ao filtro atual,
                // ela desaparece da lista automaticamente.
                this.activeIndex = Math.max(
                    0,
                    Math.min(this.activeIndex, this.ordensFiltradas.length - 1)
                );

                this.$nextTick(() => {
                    if (this.ordensFiltradas.length > 0) {
                        this.centralizarCard(this.activeIndex, false);
                    }
                });
            } catch (error) {
                console.error("Erro ao atualizar status:", error);

                alert("Não foi possível atualizar o status da ordem.");
            } finally {
                this.atualizando = null;
            }
        },

        statusClass(status) {
            const classes = {
                PENDENTE: "bg-yellow-100 text-yellow-700",
                CONCLUIDO: "bg-green-100 text-green-700",
                CANCELADO: "bg-red-100 text-red-700"
            };

            return classes[status] || "bg-gray-100 text-gray-600";
        },

        formatarStatus(status) {
            const nomes = {
                TODAS: "todas",
                PENDENTE: "pendente",
                CONCLUIDO: "concluída",
                CANCELADO: "cancelada"
            };

            return nomes[status] || status;
        },

        formatarData(data) {
            if (!data) return "Não informado";

            const partes = data.split("-");

            if (partes.length === 3) {
                return `${partes[2].substring(0, 2)}/${partes[1]}/${partes[0]}`;
            }

            return new Date(data).toLocaleDateString("pt-BR");
        },

        navegar(direcao) {
            const proximo = this.activeIndex + direcao;

            if (
                proximo < 0 ||
                proximo >= this.ordensFiltradas.length
            ) {
                return;
            }

            this.irPara(proximo);
        },

        irPara(index) {
            this.centralizarCard(index);
        },

        centralizarCard(index, animar = true) {
            const carousel = this.$refs.carousel;

            if (!carousel) return;

            if (
                index < 0 ||
                index >= this.ordensFiltradas.length
            ) {
                return;
            }

            this.activeIndex = index;

            this.$nextTick(() => {
                requestAnimationFrame(() => {
                    const card = carousel.children[index];

                    if (!card) return;

                    if (this.ordensFiltradas.length === 1) {
                        carousel.scrollTo({
                            left: 0,
                            behavior: "auto"
                        });

                        return;
                    }

                    const carouselRect = carousel.getBoundingClientRect();
                    const cardRect = card.getBoundingClientRect();

                    const centroCard =
                        cardRect.left -
                        carouselRect.left +
                        carousel.scrollLeft +
                        cardRect.width / 2;

                    const posicaoCentralizada =
                        centroCard - carousel.clientWidth / 2;

                    const limiteMaximo =
                        carousel.scrollWidth - carousel.clientWidth;

                    const posicaoFinal = Math.max(
                        0,
                        Math.min(posicaoCentralizada, limiteMaximo)
                    );

                    carousel.scrollTo({
                        left: posicaoFinal,
                        behavior: animar ? "smooth" : "auto"
                    });
                });
            });
        },

        atualizarCardAtivo() {
            const carousel = this.$refs.carousel;

            if (
                !carousel ||
                this.ordensFiltradas.length <= 1
            ) {
                this.activeIndex = 0;
                return;
            }

            if (this.scrollTimer) {
                clearTimeout(this.scrollTimer);
            }

            this.scrollTimer = setTimeout(() => {
                const carouselRect = carousel.getBoundingClientRect();
                const centroCarousel =
                    carouselRect.left + carousel.clientWidth / 2;

                let menorDistancia = Infinity;
                let indiceMaisProximo = this.activeIndex;

                Array.from(carousel.children).forEach((card, index) => {
                    const rect = card.getBoundingClientRect();
                    const centroCard = rect.left + rect.width / 2;

                    const distancia = Math.abs(
                        centroCarousel - centroCard
                    );

                    if (distancia < menorDistancia) {
                        menorDistancia = distancia;
                        indiceMaisProximo = index;
                    }
                });

                this.activeIndex = indiceMaisProximo;
            }, 100);
        },

        recentralizarCard() {
            if (this.ordensFiltradas.length > 0) {
                this.centralizarCard(this.activeIndex, false);
            }
        }
    }
};
</script>

<style scoped>
/* ÁREA DO CARROSSEL */
.carousel-container {
    position: relative;
    overflow-x: auto;
    overflow-y: hidden;

    scrollbar-width: none;
    -ms-overflow-style: none;

    scroll-behavior: smooth;
    scroll-snap-type: x mandatory;

    padding-inline: 12%;
    box-sizing: border-box;

    isolation: isolate;
}

.carousel-container::-webkit-scrollbar {
    display: none;
}

/* CARD PADRÃO */
.carousel-card {
    flex: 0 0 76%;
    width: 76%;
    min-width: 76%;

    scroll-snap-align: center;
    scroll-snap-stop: always;

    transform: scale(0.84);
    transform-origin: center center;

    opacity: 0.55;

    transition:
        transform 0.45s cubic-bezier(0.2, 0.8, 0.2, 1),
        opacity 0.45s ease,
        box-shadow 0.45s ease,
        border-color 0.45s ease;

    will-change: transform;
}

/* CARD ATIVO */
.carousel-card-active {
    transform: scale(1);
    transform-origin: center center;

    opacity: 1;
    z-index: 2;

    border-color: #86efac;

    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.10);
}

/* CARDS INATIVOS */
.carousel-card-inactive {
    transform: scale(0.84);
    transform-origin: center center;

    opacity: 0.55;

    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

/* APENAS UM CARD */
.carousel-container-single {
    overflow: visible;
    justify-content: center;
    padding-inline: 0;
    scroll-snap-type: none;
}

.carousel-card-single {
    flex: 0 1 76%;
    width: 76%;
    min-width: 0;
    max-width: 760px;

    min-height: 480px;

    display: flex;
    flex-direction: column;

    padding: 24px;

    transform: none;
    transform-origin: center center;

    opacity: 1;

    cursor: default;
    z-index: 1;
}

/* Mantém o campo de atualização próximo à parte inferior */
.carousel-card-single > div:last-child {
    margin-top: auto;
}

/* TABLETS E DESKTOPS */
@media (min-width: 640px) {
    .carousel-container {
        padding-inline: 12%;
    }

    .carousel-card {
        flex-basis: 76%;
        width: 76%;
        min-width: 76%;
    }

    .carousel-card-inactive {
        transform: scale(0.84);
    }

    .carousel-container-single {
        padding-inline: 0;
    }

    .carousel-card-single {
        flex-basis: 76%;
        width: 76%;
        min-height: 480px;
        padding: 28px;
    }
}

/* CELULARES */
@media (max-width: 639px) {
    .carousel-container {
        padding-inline: 8%;
    }

    .carousel-card {
        flex-basis: 84%;
        width: 84%;
        min-width: 84%;
    }

    .carousel-card-inactive {
        transform: scale(0.82);
    }

    .carousel-container-single {
        padding-inline: 0;
    }

    .carousel-card-single {
        flex-basis: 100%;
        width: 100%;
        max-width: 100%;
        min-height: 520px;
        padding: 20px;
    }
}
</style>
