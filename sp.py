import requests
import pandas as pd
import sys
import os

URL = "https://archive-api.open-meteo.com/v1/archive"
# Caminho da pasta config
caminho_pasta = os.path.join(
    os.path.dirname(__file__),
    "config"
)

sys.path.insert(0, caminho_pasta)

from config import (
    LATITUDE,
    LONGITUDE,
    DATA_INICIAL,
    DATA_FINAL,
    VARIAVEIS
)


parametros = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": f"2026-{DATA_INICIAL}",
    "end_date": f"2026-{DATA_FINAL}",
    "daily": ",".join(VARIAVEIS),
    "timezone": "America/Sao_Paulo"
}

def buscar_dados(ano): 
    parametros = { 
        "latitude": LATITUDE, 
        "longitude": LONGITUDE, 
        "start_date": f"{ano}-{DATA_INICIAL}", 
        "end_date": f"{ano}-{DATA_FINAL}", 
        "daily": ",".join(VARIAVEIS), 
        "timezone": "America/Sao_Paulo" 
        } 
    resposta = requests.get( URL, params=parametros )
    dados = resposta.json() 
    df = pd.DataFrame( dados["daily"] ) 
    return df 

t_sp_25_ing = buscar_dados(2025)
t_sp_26_ing = buscar_dados(2026)


print(t_sp_25_ing.isnull().sum())
print(t_sp_25_ing.duplicated().sum())

t_sp_25_ing.to_csv(
    "t_sp_25_ing.csv",
    index=False
)

t_sp_26_ing.to_csv(
    "t_sp_26_ing.csv",
    index=False
)
def classificar_direcao(graus):

    if graus >= 337.5 or graus < 22.5:
        return "Norte"

    elif graus < 67.5:
        return "Nordeste"

    elif graus < 112.5:
        return "Leste"

    elif graus < 157.5:
        return "Sudeste"

    elif graus < 202.5:
        return "Sul"

    elif graus < 247.5:
        return "Sudoeste"

    elif graus < 292.5:
        return "Oeste"

    else:
        return "Noroeste"
t_sp_25_ing["direcao_cardinal"] = t_sp_25_ing[
    "wind_direction_10m_dominant"
].apply(classificar_direcao)

t_sp_26_ing["direcao_cardinal"] = t_sp_26_ing[
    "wind_direction_10m_dominant"
].apply(classificar_direcao)

t_sp_25_ing = t_sp_25_ing.rename(columns={"time": "Data",
                                           "temperature_2m_mean": "Temperatura_media",
                                             "temperature_2m_max": "Temperatura_maxima",
                                               "temperature_2m_min": "Temperatura_minima",
                                                "wind_direction_10m_dominant": "Direcao_vento",
                                                "wind_speed_10m_mean": "Velocidade_vento"
                                                })

t_sp_26_ing = t_sp_26_ing.rename(columns={"time": "Data",
                                           "temperature_2m_mean": "Temperatura_media",
                                             "temperature_2m_max": "Temperatura_maxima",
                                               "temperature_2m_min": "Temperatura_minima",
                                                "wind_direction_10m_dominant": "Direcao_vento",
                                                "wind_speed_10m_mean": "Velocidade_vento"
                                                })

t_sp_25_ing.to_csv(
    "t_sp_25_tgt.csv",
    index=False
)

t_sp_26_ing.to_csv(
    "t_sp_26_tgt.csv",
    index=False
)