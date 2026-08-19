import pandas as pd


# ============================================================
# CONFIGURAÇÕES
# ============================================================

ANO_PASSADO = 2025
ANO_ATUAL = 2026


# ============================================================
# CARREGAR DADOS
# ============================================================

def carregar_dados():

    dataframe = pd.read_csv("dados_climaticos.csv")

    dataframe["time"] = pd.to_datetime(
        dataframe["time"]
    )

    return dataframe


# ============================================================
# PREPARAR DATA PARA COMPARAÇÃO
# ============================================================

def preparar_dados(dataframe):

    dataframe = dataframe.copy()

    # Cria uma data de comparação.
    # Exemplo:
    #
    # 2025-06-01 -> 06-01
    # 2026-06-01 -> 06-01
    #
    # Assim conseguimos comparar exatamente
    # o mesmo dia de cada ano.

    dataframe["mes_dia"] = dataframe["time"].dt.strftime(
        "%m-%d"
    )

    return dataframe


# ============================================================
# SEPARAR 2025 E 2026
# ============================================================

def separar_anos(dataframe):

    dados_2025 = dataframe[
        dataframe["ano"] == ANO_PASSADO
    ].copy()

    dados_2026 = dataframe[
        dataframe["ano"] == ANO_ATUAL
    ].copy()

    return dados_2025, dados_2026


# ============================================================
# CRIAR COMPARAÇÃO
# ============================================================

def criar_comparacao(dataframe):

    dados_2025, dados_2026 = separar_anos(
        dataframe
    )

    colunas_comparacao = [
        "mes_dia",
        "estado",
        "capital",
        "regiao",
        "temperature_2m_mean",
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "relative_humidity_2m_mean",
        "wind_speed_10m_mean"
    ]

    dados_2025 = dados_2025[
        colunas_comparacao
    ].copy()

    dados_2026 = dados_2026[
        colunas_comparacao
    ].copy()


    # Renomear variáveis de 2025

    dados_2025 = dados_2025.rename(
        columns={
            "temperature_2m_mean": "temp_media_2025",
            "temperature_2m_max": "temp_max_2025",
            "temperature_2m_min": "temp_min_2025",
            "precipitation_sum": "chuva_2025",
            "relative_humidity_2m_mean": "umidade_2025",
            "wind_speed_10m_mean": "vento_2025"
        }
    )


    # Renomear variáveis de 2026

    dados_2026 = dados_2026.rename(
        columns={
            "temperature_2m_mean": "temp_media_2026",
            "temperature_2m_max": "temp_max_2026",
            "temperature_2m_min": "temp_min_2026",
            "precipitation_sum": "chuva_2026",
            "relative_humidity_2m_mean": "umidade_2026",
            "wind_speed_10m_mean": "vento_2026"
        }
    )


    # ========================================================
    # JUNTAR OS DOIS ANOS
    # ========================================================

    comparacao = pd.merge(
        dados_2025,
        dados_2026,
        on=[
            "mes_dia",
            "estado",
            "capital",
            "regiao"
        ],
        how="inner"
    )


    # ========================================================
    # DIFERENÇAS
    # ========================================================

    comparacao["dif_temp_media"] = (
        comparacao["temp_media_2026"]
        - comparacao["temp_media_2025"]
    )


    comparacao["dif_temp_max"] = (
        comparacao["temp_max_2026"]
        - comparacao["temp_max_2025"]
    )


    comparacao["dif_temp_min"] = (
        comparacao["temp_min_2026"]
        - comparacao["temp_min_2025"]
    )


    comparacao["dif_chuva"] = (
        comparacao["chuva_2026"]
        - comparacao["chuva_2025"]
    )


    comparacao["dif_umidade"] = (
        comparacao["umidade_2026"]
        - comparacao["umidade_2025"]
    )


    comparacao["dif_vento"] = (
        comparacao["vento_2026"]
        - comparacao["vento_2025"]
    )


    # ========================================================
    # VARIAÇÃO PERCENTUAL DA CHUVA
    # ========================================================

    comparacao["variacao_chuva_percentual"] = (
        (
            comparacao["chuva_2026"]
            - comparacao["chuva_2025"]
        )
        / comparacao["chuva_2025"]
    ) * 100


    # ========================================================
    # ARREDONDAMENTO
    # ========================================================

    colunas_numericas = [
        "temp_media_2025",
        "temp_max_2025",
        "temp_min_2025",
        "chuva_2025",
        "umidade_2025",
        "vento_2025",
        "temp_media_2026",
        "temp_max_2026",
        "temp_min_2026",
        "chuva_2026",
        "umidade_2026",
        "vento_2026",
        "dif_temp_media",
        "dif_temp_max",
        "dif_temp_min",
        "dif_chuva",
        "dif_umidade",
        "dif_vento",
        "variacao_chuva_percentual"
    ]

    comparacao[colunas_numericas] = (
        comparacao[colunas_numericas]
        .round(2)
    )


    return comparacao


# ============================================================
# RESUMO POR ESTADO
# ============================================================

def resumo_estados(comparacao):

    resumo = comparacao.groupby(
        [
            "estado",
            "capital",
            "regiao"
        ]
    ).agg({

        "temp_media_2025": "mean",
        "temp_media_2026": "mean",

        "temp_max_2025": "mean",
        "temp_max_2026": "mean",

        "temp_min_2025": "mean",
        "temp_min_2026": "mean",

        "chuva_2025": "sum",
        "chuva_2026": "sum",

        "umidade_2025": "mean",
        "umidade_2026": "mean",

        "vento_2025": "mean",
        "vento_2026": "mean"

    }).reset_index()


    # Diferenças

    resumo["dif_temp_media"] = (
        resumo["temp_media_2026"]
        - resumo["temp_media_2025"]
    )

    resumo["dif_temp_max"] = (
        resumo["temp_max_2026"]
        - resumo["temp_max_2025"]
    )

    resumo["dif_temp_min"] = (
        resumo["temp_min_2026"]
        - resumo["temp_min_2025"]
    )

    resumo["dif_chuva"] = (
        resumo["chuva_2026"]
        - resumo["chuva_2025"]
    )

    resumo["dif_umidade"] = (
        resumo["umidade_2026"]
        - resumo["umidade_2025"]
    )

    resumo["dif_vento"] = (
        resumo["vento_2026"]
        - resumo["vento_2025"]
    )


    resumo["variacao_chuva_percentual"] = (
        (
            resumo["chuva_2026"]
            - resumo["chuva_2025"]
        )
        / resumo["chuva_2025"]
    ) * 100


    return resumo.round(2)


# ============================================================
# RESUMO POR REGIÃO
# ============================================================

def resumo_regioes(comparacao):

    resumo = comparacao.groupby(
        "regiao"
    ).agg({

        "temp_media_2025": "mean",
        "temp_media_2026": "mean",

        "temp_max_2025": "mean",
        "temp_max_2026": "mean",

        "temp_min_2025": "mean",
        "temp_min_2026": "mean",

        "chuva_2025": "mean",
        "chuva_2026": "mean",

        "umidade_2025": "mean",
        "umidade_2026": "mean",

        "vento_2025": "mean",
        "vento_2026": "mean"

    }).reset_index()


    resumo["dif_temp_media"] = (
        resumo["temp_media_2026"]
        - resumo["temp_media_2025"]
    )

    resumo["dif_temp_max"] = (
        resumo["temp_max_2026"]
        - resumo["temp_max_2025"]
    )

    resumo["dif_temp_min"] = (
        resumo["temp_min_2026"]
        - resumo["temp_min_2025"]
    )

    resumo["dif_chuva"] = (
        resumo["chuva_2026"]
        - resumo["chuva_2025"]
    )

    resumo["dif_umidade"] = (
        resumo["umidade_2026"]
        - resumo["umidade_2025"]
    )

    resumo["dif_vento"] = (
        resumo["vento_2026"]
        - resumo["vento_2025"]
    )


    return resumo.round(2)


# ============================================================
# EXECUÇÃO
# ============================================================

df = carregar_dados()

df = preparar_dados(df)

comparacao = criar_comparacao(df)

estados_comparacao = resumo_estados(
    comparacao
)

regioes_comparacao = resumo_regioes(
    comparacao
)


# ============================================================
# SALVAR RESULTADOS
# ============================================================

comparacao.to_csv(
    "comparacao_diaria_2025_2026.csv",
    index=False
)

estados_comparacao.to_csv(
    "comparacao_por_estado.csv",
    index=False
)

regioes_comparacao.to_csv(
    "comparacao_por_regiao.csv",
    index=False
)


# ============================================================
# EXIBIR RESULTADOS
# ============================================================

print("\n===== COMPARAÇÃO DIÁRIA =====")
print(comparacao.head())

print("\n===== COMPARAÇÃO POR ESTADO =====")
print(estados_comparacao)

print("\n===== COMPARAÇÃO POR REGIÃO =====")
print(regioes_comparacao)
