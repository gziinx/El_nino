"""BRONZE: baixa os dados brutos da API Open-Meteo -> arquivos/bronze/."""
import logging

import pandas as pd
import requests

from config import config as cfg

log = logging.getLogger(__name__)


def buscar_dados(ano: int) -> pd.DataFrame:
    """Baixa os dados diários do ano escolhido (no período definido em config)."""
    parametros = {
        "latitude": cfg.LATITUDE,
        "longitude": cfg.LONGITUDE,
        "start_date": f"{ano}-{cfg.DATA_INICIAL}",
        "end_date": f"{ano}-{cfg.DATA_FINAL}",
        "daily": ",".join(cfg.VARIAVEIS),
        "timezone": cfg.TIMEZONE,
    }
    resposta = requests.get(cfg.URL_API, params=parametros, timeout=60)
    if not resposta.ok:
        raise RuntimeError(f"API retornou erro {resposta.status_code} para {ano}: {resposta.text[:300]}")
    dados = resposta.json()
    if "daily" not in dados:
        raise ValueError(f"Resposta da API sem 'daily' para {ano}: {dados}")
    df = pd.DataFrame(dados["daily"])
    if df.empty:
        raise ValueError(f"A API não devolveu nenhum dado para {ano}.")
    return df


def executar(ano: int):
    cfg.DIR_BRONZE.mkdir(parents=True, exist_ok=True)
    df = buscar_dados(ano)
    destino = cfg.DIR_BRONZE / cfg.nome_arquivo(ano, "bronze")
    df.to_csv(destino, index=False)
    log.info("[bronze] %s: %d linhas -> %s", ano, len(df), destino)
    return destino
