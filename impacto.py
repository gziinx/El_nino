import requests
import pandas as pd

from estados import estados


DATA_INICIAL = "06-01"
DATA_FINAL = "08-19"


def buscar_clima(nome_estado, dados_estado, ano):

    inicio = f"{ano}-{DATA_INICIAL}"
    fim = f"{ano}-{DATA_FINAL}"

    url = "https://archive-api.open-meteo.com/v1/archive"

    parametros = {
        "latitude": dados_estado["latitude"],
        "longitude": dados_estado["longitude"],
        "start_date": inicio,
        "end_date": fim,
        "daily": [
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "relative_humidity_2m_mean",
            "wind_speed_10m_mean"
        ],
        "timezone": "America/Sao_Paulo"
    }

    resposta = requests.get(url, params=parametros)

    resposta.raise_for_status()

    dados = resposta.json()

    dataframe = pd.DataFrame(dados["daily"])

    dataframe["time"] = pd.to_datetime(dataframe["time"])

    dataframe["estado"] = nome_estado
    dataframe["capital"] = dados_estado["capital"]
    dataframe["regiao"] = dados_estado["regiao"]
    dataframe["ano"] = ano

    return dataframe

def coletar_dados():

    dados = []

    for estado, informacoes in estados.items():

        print(f"Buscando dados de {estado}...")

        dados_2025 = buscar_clima(
            estado,
            informacoes,
            2025
        )

        dados_2026 = buscar_clima(
            estado,
            informacoes,
            2026
        )

        dados.append(dados_2025)
        dados.append(dados_2026)

    dataframe = pd.concat(
        dados,
        ignore_index=True
    )

    return dataframe

df = coletar_dados()

print(df.head())

df.to_csv(
    "dados_climaticos.csv",
    index=False
)