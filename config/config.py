"""Configurações do pipeline El Niño (São Paulo).

O ano NÃO fica aqui: ele é passado na hora de rodar (ver run_pipeline.py).
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Camadas (arquitetura medalhão) -----------------------------------------
DIR_BRONZE = BASE_DIR / "arquivos" / "bronze"   # bruto, como veio da API
DIR_SILVER = BASE_DIR / "arquivos" / "silver"   # limpo, tipado, colunas em português
DIR_GOLD = BASE_DIR / "arquivos" / "gold"       # enriquecido, pronto para uso

# --- API Open-Meteo (histórico) ---------------------------------------------
URL_API = "https://archive-api.open-meteo.com/v1/archive"
TIMEZONE = "America/Sao_Paulo"
LATITUDE = -23.5505   # São Paulo
LONGITUDE = -46.6333

# Período (MM-DD) aplicado ao ano escolhido. Pode ser sobrescrito por linha de comando.
DATA_INICIAL = "06-01"
DATA_FINAL = "08-31"

# Mínimo/máximo de anos que a API histórica cobre
ANO_MINIMO = 1940

# Variáveis pedidas à API.
# Obs.: 'precipitation_probability_max' foi removida: ela só existe na API de
# PREVISÃO; a API histórica não a fornece (vinha sempre vazia / podia dar erro).
VARIAVEIS = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "wind_direction_10m_dominant",
    "wind_speed_10m_mean",
    "rain_sum",
]

COLUNAS_PT = {
    "time": "Data",
    "temperature_2m_mean": "Temperatura_media",
    "temperature_2m_max": "Temperatura_maxima",
    "temperature_2m_min": "Temperatura_minima",
    "wind_direction_10m_dominant": "Direcao_vento",
    "wind_speed_10m_mean": "Velocidade_vento",
    "rain_sum": "Soma_chuva",
}


def nome_arquivo(ano: int, camada: str) -> str:
    """Inclui o período no nome. Ex.: 'sp_1982_0601_0826_silver.csv'."""
    ini = DATA_INICIAL.replace("-", "")
    fim = DATA_FINAL.replace("-", "")
    return f"sp_{ano}_{ini}_{fim}_{camada}.csv"
