
<template>
    <Navbar />

    <main class="min-h-[calc(100dvh-80px)] bg-gray-50 px-6 py-10 md:px-12">

        <!-- Cabeçalho -->
        <section class="max-w-5xl mx-auto mb-8">
            <button
                @click="$router.push('/ativos')"
                class="flex items-center gap-2 text-gray-600 hover:text-gray-900
                       transition cursor-pointer mb-6"
            >
                Voltar para ativos
            </button>

            <h1 class="text-3xl font-bold text-center text-gray-800">
                Detalhes do ativo
            </h1>
        </section>

        <!-- Carregamento -->
        <section
            v-if="loading"
            class="max-w-5xl mx-auto bg-white rounded-xl border border-gray-200
                   p-10 text-center text-gray-400"
        >
            Carregando informações do ativo...
        </section>

        <!-- Erro -->
        <section
            v-else-if="error"
            class="max-w-5xl mx-auto bg-white rounded-xl border border-gray-200
                   p-10 text-center"
        >
            <p class="text-red-500 mb-5">
                {{ error }}
            </p>

            <button
                @click="fetchAsset"
                class="px-5 py-2.5 rounded-lg bg-[#E5F8EC]
                       text-gray-700 font-semibold hover:bg-[#d2f0dc]
                       transition cursor-pointer"
            >
                Tentar novamente
            </button>
        </section>

        <!-- Informações do ativo -->
        <section
            v-else-if="asset"
            class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2
                   gap-6 items-start"
        >

            <!-- QR Code -->
            <div class="bg-white rounded-xl border border-gray-200
                        p-8 flex flex-col items-center">

                <h2 class="text-xl font-semibold text-gray-800 mb-2">
                    QR Code do ativo
                </h2>

                <div class="bg-white border border-gray-100 rounded-xl p-4">
                    <QrcodeVue
                        :value="qrContent"
                        :size="240"
                        level="H"
                        render-as="svg"
                    />
                </div>

                <p class="text-sm font-semibold text-gray-700 mt-5">
                    Patrimônio: {{ asset.patrimonio }}
                </p>

                <p class="text-xs text-gray-400 mt-2 text-center">
                    Escaneie o código para consultar os dados do ativo.
                </p>

            </div>

            <!-- Dados do ativo -->
            <div class="bg-white rounded-xl border border-gray-200 p-8">

                <div class="flex items-center justify-between gap-3 mb-6">
                    <h2 class="text-xl font-semibold text-gray-800">
                        Informações
                    </h2>

                    <span
                        class="px-3 py-1 rounded-full text-xs font-semibold"
                        :class="statusClass(asset.status)"
                    >
                        {{ statusLabel(asset.status) }}
                    </span>
                </div>

                <div class="space-y-5">

                    <div>
                        <p class="text-sm text-gray-400 mb-1">
                            Patrimônio
                        </p>
                        <p class="font-semibold text-gray-800">
                            {{ asset.patrimonio }}
                        </p>
                    </div>

                    <div>
                        <p class="text-sm text-gray-400 mb-1">
                            Nome
                        </p>
                        <p class="font-semibold text-gray-800">
                            {{ asset.nome }}
                        </p>
                    </div>

                    <div>
                        <p class="text-sm text-gray-400 mb-1">
                            Descrição
                        </p>
                        <p class="text-gray-700">
                            {{ asset.descricao || '-' }}
                        </p>
                    </div>

                    <div>
                        <p class="text-sm text-gray-400 mb-1">
                            Categoria
                        </p>
                        <p class="text-gray-700">
                            {{ asset.categoriaNome }}
                        </p>
                    </div>

                    <div>
                        <p class="text-sm text-gray-400 mb-1">
                            Laboratório
                        </p>
                        <p class="text-gray-700">
                            {{ asset.laboratorioNome }}
                        </p>
                    </div>

                </div>

            </div>

        </section>

    </main>
</template>

<script>
import Navbar from "../components/navbarVue.vue";
import QrcodeVue from "qrcode.vue";
import api from "../services/api.js";

export default {
    name: "AtivoDetalhes",

    components: {
        Navbar,
        QrcodeVue
    },

    data() {
        return {
            asset: null,
            loading: false,
            error: null
        };
    },

    computed: {
        // Conteúdo exclusivo do QR Code
        qrContent() {
            if (!this.asset) {
                return "";
            }

            return JSON.stringify({
                id: this.asset.id,
                patrimonio: this.asset.patrimonio,
                nome: this.asset.nome,
                descricao: this.asset.descricao,
                categoria: this.asset.categoriaNome,
                laboratorio: this.asset.laboratorioNome
            });
        }
    },

    async mounted() {
        await this.fetchAsset();
    },

    methods: {
        async fetchAsset() {
            this.loading = true;
            this.error = null;

            try {
                const id = this.$route.params.id;

                const response = await api.get(`ativo/${id}/`);
                const item = response.data;

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

                this.asset = {
                    id: item.id,
                    patrimonio: item.patrimonio || "-",
                    nome: item.nome || "-",
                    descricao: item.descricao || "-",
                    status: item.status,
                    categoriaNome,
                    laboratorioNome
                };

            } catch (error) {
                console.error("Erro ao buscar detalhes do ativo:", error);

                this.error =
                    "Não foi possível carregar as informações deste ativo.";
            } finally {
                this.loading = false;
            }
        },

        statusLabel(status) {
            const labels = {
                DISPONIVEL: "Disponível",
                INDISPONIVEL: "Indisponível",
                MANUTENCAO: "Manutenção"
            };

            return labels[status] || "Não informado";
        },

        statusClass(status) {
            const classes = {
                DISPONIVEL: "bg-green-100 text-green-700",
                INDISPONIVEL: "bg-red-100 text-red-700",
                MANUTENCAO: "bg-blue-100 text-blue-700"
            };

            return classes[status] || "bg-gray-100 text-gray-600";
        },

        // Baixar QR Code como imagem PNG
        downloadQrCode() {
            const svg = document.querySelector(".qrcode svg");

            // Busca o SVG gerado pelo componente
            const qrSvg = document.querySelector(
                'svg[viewBox]'
            );

            if (!qrSvg) {
                alert("Não foi possível gerar o arquivo do QR Code.");
                return;
            }

            const serializer = new XMLSerializer();
            const svgString = serializer.serializeToString(qrSvg);

            const svgBlob = new Blob(
                [svgString],
                { type: "image/svg+xml;charset=utf-8" }
            );

            const url = URL.createObjectURL(svgBlob);
            const image = new Image();

            image.onload = () => {
                const canvas = document.createElement("canvas");
                canvas.width = 500;
                canvas.height = 500;

                const context = canvas.getContext("2d");

                context.fillStyle = "#FFFFFF";
                context.fillRect(0, 0, canvas.width, canvas.height);

                context.drawImage(image, 0, 0, 500, 500);

                const link = document.createElement("a");
                link.download = `qrcode-ativo-${this.asset.patrimonio}.png`;
                link.href = canvas.toDataURL("image/png");
                link.click();

                URL.revokeObjectURL(url);
            };

            image.onerror = () => {
                URL.revokeObjectURL(url);
                alert("Não foi possível baixar o QR Code.");
            };

            image.src = url;
        }
    }
};
</script>
