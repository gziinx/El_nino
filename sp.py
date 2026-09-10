# Import para o cunsumo da api(request),  
# Import para utilizar dados de outro arquivo(os, sys)
# Import para manipular os dados (pandas pd)
import requests
import pandas as pd
import sys
import os

# Consumo da api
URL = "https://archive-api.open-meteo.com/v1/archive"

# Pegando dados fixos do aruivo config.py
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

# Função com filtro de ano, e transforma em dataframe
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

# Usando a função 
t_sp_25_ing = buscar_dados(2025)
t_sp_26_ing = buscar_dados(2026)

# Etapa bronze concluida (dados brutos de 2025 e 2026 em csv)
t_sp_25_ing.to_csv(
    "t_sp_25_ing.csv",
    index=False
)

t_sp_26_ing.to_csv(
    "t_sp_26_ing.csv",
    index=False
)

#
# ETAPA SILVER
#


# Verificando se tem dados vazios
print(t_sp_25_ing.isnull().sum())

# Verificando se tem dados duplicados
print(t_sp_25_ing.duplicated().sum())

# Verificando a tipagem e etc... 
print(t_sp_25_ing.info())
print(t_sp_26_ing.info())

# Alterando o tipo da data que estava str
t_sp_25_ing["Data"] = pd.to_datetime(
        t_sp_25_ing["Data"],
        format="%Y-%m-%d",
        errors="raise"
    )

t_sp_26_ing["Data"] = pd.to_datetime(
        t_sp_26_ing["Data"],
        format="%Y-%m-%d",
        errors="raise"
    )

# Traduzindo as colunas
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


#
# Exportando a etapa silver
#
t_sp_25_ing.to_csv(
    "t_sp_25_tgt.csv",
    index=False
)

t_sp_26_ing.to_csv(
    "t_sp_26_tgt.csv",
    index=False
)
