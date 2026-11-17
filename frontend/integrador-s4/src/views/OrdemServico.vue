
<template>
    <Navbar />

    <main class="min-h-[calc(100dvh-80px)] bg-gray-50 px-5 pt-3 pb-2 md:px-12">
        <!-- Cabeçalho -->
        <section class="mx-auto mb-6 max-w-7xl">
            <div class="flex flex-col justify-between gap-4 md:flex-row md:items-center">
                <div>
                    <h1 class="text-2xl font-bold text-gray-800 md:text-3xl">
                        Ordens de Serviço
                    </h1>
                </div>

                <!-- Total e ações -->
                <div class="flex flex-wrap items-center gap-3">
                    <button
                        @click="abrirFormulario"
                        class="flex items-center gap-2 rounded-xl bg-green-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-green-700"
                    >
                        <span class="text-lg">+</span>
                        Adicionar
                    </button>

                    <button
                        @click="removerOrdem"
                        :disabled="ordens.length === 0"
                        class="flex items-center gap-2 rounded-xl bg-red-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                        <span class="text-lg">−</span>
                        Remover
                    </button>

                    <div class="flex items-center gap-3 rounded-xl border border-gray-200 bg-white px-5 py-3 shadow-sm">
                        <div>
                            <p class="text-xs text-gray-500">Total de ordens</p>
                            <p class="text-center text-xl font-bold text-gray-800">
                                {{ ordens.length }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Conteúdo principal -->
        <section class="mx-auto max-w-7xl">

            <!-- Carregamento -->
            <div
                v-if="loading"
                class="flex min-h-[50vh] items-center justify-center"
            >
                <div class="text-center">
                    <div class="mx-auto mb-3 h-9 w-9 animate-spin rounded-full border-4 border-gray-200 border-t-green-500"></div>

                    <p class="text-sm text-gray-500">
                        Carregando ordens de serviço...
                    </p>
                </div>
            </div>

            <!-- Erro -->
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

            <!-- Estado vazio -->
            <div
                v-else-if="ordens.length === 0"
                class="flex min-h-[50vh] flex-col items-center justify-center rounded-xl border border-gray-200 bg-white p-8 text-center"
            >
                <h3 class="font-semibold text-gray-700">
                    Nenhuma ordem encontrada
                </h3>

                <p class="mt-1 text-sm text-gray-500">
                    Ainda não existem ordens de serviço cadastradas.
                </p>
            </div>

            <!-- Carrossel -->
            <div
                v-else
                class="mx-auto flex w-full max-w-6xl items-center justify-center gap-2 sm:gap-5"
            >
                <!-- Seta esquerda -->
                <button
                    v-if="ordens.length > 1"
                    @click="navegar(-1)"
                    :disabled="activeIndex === 0"
                    class="z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-gray-200 bg-white text-gray-700 shadow-md transition hover:border-green-400 hover:bg-green-50 hover:text-green-700 disabled:cursor-not-allowed disabled:opacity-30 sm:h-12 sm:w-12"
                    aria-label="Ordem anterior"
                >
                    <span class="text-3xl leading-none">‹</span>
                </button>

                <!-- Área visível do carrossel -->
                <div
                    ref="carousel"
                    class="flex min-w-0 flex-1 items-center gap-5 overflow-hidden py-5 px-[calc((100%_-_420px)/2)] max-sm:gap-4 max-sm:px-[calc((100%_-_290px)/2)]"
                >
                    <article
                        v-for="(ordem, index) in ordens"
                        :key="ordem.id"
                        @click="irPara(index)"
                        class="w-[290px] min-w-[290px] cursor-pointer rounded-2xl border border-gray-200 bg-white p-4 opacity-50 scale-[0.90] shadow-sm transition-all duration-300 ease-in-out sm:w-[420px] sm:min-w-[420px] sm:p-5"
                        :class="{
                            '!scale-100 !opacity-100 !border-green-200 !shadow-xl':
                                index === activeIndex
                        }"
                    >
                        <!-- Identificação -->
                        <div class="mb-4 flex items-center justify-between">
                            <span class="text-xs font-semibold uppercase tracking-wider text-gray-400">
                                Ordem #{{ ordem.id }}
                            </span>

                            <span
                                class="rounded-full px-3 py-1 text-xs font-semibold"
                                :class="statusClass(ordem.status)"
                            >
                                {{ formatarStatus(ordem.status) }}
                            </span>
                        </div>

                        <!-- Ativo -->
                        <div class="mb-4">
                            <p class="mb-1 text-xs font-semibold uppercase tracking-wide text-gray-400">
                                Ativo em manutenção
                            </p>

                            <h3 class="text-lg font-bold text-gray-800">
                                {{ getAtivo(ordem).nome || "Ativo não informado" }}
                            </h3>

                            <div class="mt-1 flex items-center gap-2">
                                <span class="text-xs text-gray-500">
                                    Patrimônio:
                                </span>

                                <span class="rounded bg-gray-100 px-2 py-1 text-xs font-semibold text-gray-700">
                                    {{ getAtivo(ordem).patrimonio || "Não informado" }}
                                </span>
                            </div>
                        </div>

                        <!-- Laboratórios -->
                        <div class="mb-4 grid grid-cols-2 gap-3 rounded-xl bg-gray-50 p-3">
                            <div>
                                <p class="mb-2 text-xs font-medium text-gray-400">
                                    Origem
                                </p>

                                <p class="break-words text-sm font-semibold text-gray-700">
                                    {{ getLaboratorio(ordem, "origem") }}
                                </p>
                            </div>

                            <div>
                                <p class="mb-2 text-xs font-medium text-gray-400">
                                    Destino
                                </p>

                                <p class="break-words text-sm font-semibold text-gray-700">
                                    {{ getLaboratorio(ordem, "destino") }}
                                </p>
                            </div>
                        </div>

                        <!-- Descrição -->
                        <div class="mb-4">
                            <p class="mb-1 text-xs font-semibold uppercase tracking-wide text-gray-400">
                                Descrição
                            </p>

                            <p class="line-clamp-2 min-h-10 text-sm leading-relaxed text-gray-600">
                                {{ ordem.descricao || "Nenhuma descrição informada." }}
                            </p>
                        </div>

                        <!-- Datas -->
                        <div class="mb-4 grid grid-cols-2 gap-3 border-y border-gray-100 py-3">
                            <div>
                                <p class="text-xs text-gray-400">
                                    Data de abertura
                                </p>

                                <p class="mt-1 text-sm font-semibold text-gray-700">
                                    {{ formatarData(ordem.data_abertura) }}
                                </p>
                            </div>

                            <div>
                                <p class="text-xs text-gray-400">
                                    Data de fechamento
                                </p>

                                <p class="mt-1 text-sm font-semibold text-gray-700">
                                    {{ formatarData(ordem.data_fechamento) }}
                                </p>
                            </div>
                        </div>

                        <!-- Alteração de status -->
                        <div @click.stop>
                            <label
                                :for="'status-' + ordem.id"
                                class="mb-2 block text-xs font-semibold text-gray-600"
                            >
                                Atualizar status da ordem
                            </label>

                            <select
                                :id="'status-' + ordem.id"
                                :value="ordem.status"
                                :disabled="atualizando === ordem.id"
                                @change="atualizarStatus(ordem, $event.target.value)"
                                class="w-full appearance-none rounded-lg border border-gray-200 bg-white px-3 py-2.5 text-sm text-gray-700 outline-none transition focus:border-green-400 focus:ring-2 focus:ring-green-100 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                <option value="PENDENTE">Pendente</option>
                                <option value="CONCLUIDO">Concluído</option>
                                <option value="CANCELADO">Cancelado</option>
                            </select>

                            <p
                                v-if="atualizando === ordem.id"
                                class="mt-2 text-xs text-gray-400"
                            >
                                Salvando alteração...
                            </p>
                        </div>
                    </article>
                </div>

                <!-- Seta direita -->
                <button
                    v-if="ordens.length > 1"
                    @click="navegar(1)"
                    :disabled="activeIndex === ordens.length - 1"
                    class="z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-gray-200 bg-white text-gray-700 shadow-md transition hover:border-green-400 hover:bg-green-50 hover:text-green-700 disabled:cursor-not-allowed disabled:opacity-30 sm:h-12 sm:w-12"
                    aria-label="Próxima ordem"
                >
                    <span class="text-3xl leading-none">›</span>
                </button>
            </div>

            <!-- Indicadores -->
            <div
                v-if="ordens.length > 1 && !loading && !error"
                class="mt-3 flex justify-center gap-2"
            >
                <button
                    v-for="(ordem, index) in ordens"
                    :key="ordem.id"
                    @click="irPara(index)"
                    :aria-label="'Ir para ordem ' + ordem.id"
                    class="h-2 rounded-full transition-all duration-300"
                    :class="activeIndex === index
                        ? 'w-8 bg-green-500'
                        : 'w-2 bg-gray-300 hover:bg-green-300'"
                ></button>
            </div>
        </section>
    </main>

    <!-- Modal de cadastro -->
    <Teleport to="body">
        <div
            v-if="mostrarFormulario"
            class="fixed inset-0 z-[99999] flex items-center justify-center overflow-hidden bg-black/60 p-3 sm:p-5"
            @click.self="fecharFormulario"
        >
            <section
                class="max-h-[calc(100dvh-2rem)] w-full max-w-xl overflow-y-auto overscroll-contain rounded-2xl bg-white p-6 shadow-2xl"
            >
                <div class="mb-6 flex items-center justify-between">
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
                        class="text-2xl text-gray-400 transition hover:text-gray-700"
                        aria-label="Fechar formulário"
                    >
                        &times;
                    </button>
                </div>

                <form @submit.prevent="adicionarOrdem" class="space-y-2">

                    <!-- Ativo -->
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

                        <p v-if="ativos.length === 0" class="mt-1 text-xs text-red-500">
                            Nenhum ativo disponível.
                        </p>
                    </div>

                    <!-- Usuário -->
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

                    <!-- Descrição -->
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

                    <!-- Origem e destino -->
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

                    <!-- Data de fechamento -->
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

                    <!-- Botões -->
                    <div class="flex justify-end gap-3 border-t border-gray-100 pt-5">
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

            // Cadastro
            mostrarFormulario: false,
            salvandoOrdem: false,

            // Controle do scroll da página
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
            }
        };
    },

    mounted() {
        this.buscarOrdens();
    },

    watch: {
        mostrarFormulario(aberto) {
            if (aberto) {
                // Salva a posição atual da página
                this.scrollYAnterior = window.scrollY;

                // Salva os estilos originais do body
                this.estilosBodyAnteriores = {
                    position: document.body.style.position,
                    top: document.body.style.top,
                    left: document.body.style.left,
                    right: document.body.style.right,
                    width: document.body.style.width,
                    overflow: document.body.style.overflow
                };

                // Bloqueia o scroll do conteúdo de trás
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
        // Restaura o scroll caso o componente seja desmontado
        this.restaurarScroll();
    },

    methods: {
        // Restaura os estilos e a posição original da página
        restaurarScroll() {
            if (!this.estilosBodyAnteriores) return;

            Object.assign(document.body.style, this.estilosBodyAnteriores);

            window.scrollTo(0, this.scrollYAnterior);

            this.estilosBodyAnteriores = null;
        },

        // Busca as ordens de serviço
        async buscarOrdens() {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.get("ordem-servico/");

                this.ordens = Array.isArray(response.data)
                    ? response.data
                    : response.data.results || [];

                this.$nextTick(() => {
                    if (this.ordens.length > 0) {
                        this.centralizarCard(
                            Math.min(this.activeIndex, this.ordens.length - 1)
                        );
                    } else {
                        this.activeIndex = 0;
                    }
                });

            } catch (error) {
                console.error("Erro ao buscar ordens:", error);

                if (error.response) {
                    console.error("Resposta da API:", error.response.data);

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

        // Retorna os dados do ativo
        getAtivo(ordem) {
            if (ordem.ativo_detalhes) {
                return ordem.ativo_detalhes;
            }

            if (ordem.ativo && typeof ordem.ativo === "object") {
                return ordem.ativo;
            }

            return {};
        },

        // Retorna o laboratório de origem ou destino
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

        // Abre o formulário e carrega os dados
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

        // Fecha o formulário
        fecharFormulario() {
            if (this.salvandoOrdem) return;

            this.mostrarFormulario = false;
        },

        // Valor do laboratório enviado ao backend
        laboratorioValor(laboratorio) {
            return laboratorio.nome ||
                laboratorio.codigo ||
                String(laboratorio.id);
        },

        // Nome apresentado no select
        laboratorioNome(laboratorio) {
            return laboratorio.nome ||
                laboratorio.codigo ||
                `Laboratório ${laboratorio.id}`;
        },

        // Cadastra uma nova ordem
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
                this.activeIndex = 0;

                await this.buscarOrdens();

                alert("Ordem de serviço cadastrada com sucesso!");

            } catch (error) {
                console.error("Erro ao cadastrar ordem:", error);

                if (error.response) {
                    console.error("Resposta da API:", error.response.data);

                    alert(
                        "Erro ao cadastrar ordem: " +
                        JSON.stringify(error.response.data)
                    );
                } else {
                    alert("Não foi possível conectar ao servidor.");
                }

            } finally {
                this.salvandoOrdem = false;
            }
        },

        // Remove a ordem atualmente selecionada
        async removerOrdem() {
            const ordem = this.ordens[this.activeIndex];

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
                    Math.min(this.activeIndex, this.ordens.length - 1)
                );

                this.$nextTick(() => {
                    if (this.ordens.length > 0) {
                        this.centralizarCard(this.activeIndex);
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

        // Atualiza o status da ordem
        async atualizarStatus(ordem, novoStatus) {
            const statusAnterior = ordem.status;

            if (novoStatus === statusAnterior) return;

            this.atualizando = ordem.id;

            try {
                await api.patch(`ordem-servico/${ordem.id}/`, {
                    status: novoStatus
                });

                ordem.status = novoStatus;

            } catch (error) {
                console.error("Erro ao atualizar status:", error);

                alert("Não foi possível atualizar o status da ordem.");

            } finally {
                this.atualizando = null;
            }
        },

        // Define as cores dos status
        statusClass(status) {
            const classes = {
                PENDENTE: "bg-yellow-100 text-yellow-700",
                CONCLUIDO: "bg-green-100 text-green-700",
                CANCELADO: "bg-red-100 text-red-700"
            };

            return classes[status] || "bg-gray-100 text-gray-600";
        },

        // Formata o nome do status
        formatarStatus(status) {
            const nomes = {
                PENDENTE: "Pendente",
                CONCLUIDO: "Concluído",
                CANCELADO: "Cancelado"
            };

            return nomes[status] || status;
        },

        // Formata as datas
        formatarData(data) {
            if (!data) return "Não informado";

            // Evita problemas de fuso horário com datas YYYY-MM-DD
            const partes = data.split("-");

            if (partes.length === 3) {
                return `${partes[2].substring(0, 2)}/${partes[1]}/${partes[0]}`;
            }

            return new Date(data).toLocaleDateString("pt-BR");
        },

        // Navegação pelas setas
        navegar(direcao) {
            const proximo = this.activeIndex + direcao;

            if (proximo < 0 || proximo >= this.ordens.length) return;

            this.irPara(proximo);
        },

        // Navegação pelos indicadores ou clique nos cards
        irPara(index) {
            this.centralizarCard(index);
        },

        // Centraliza o card selecionado
        centralizarCard(index) {
            const carousel = this.$refs.carousel;

            if (!carousel) return;

            const card = carousel.children[index];

            if (!card) return;

            carousel.scrollTo({
                left: card.offsetLeft -
                    (carousel.clientWidth - card.clientWidth) / 2,
                behavior: "smooth"
            });

            this.activeIndex = index;
        }
    }
};
</script>
