"""GOLD: enriquecimento (direção cardinal do vento, colunas de calendário) -> arquivos/gold/."""
import logging

import pandas as pd

from config import config as cfg

log = logging.getLogger(__name__)


def classificar_direcao(graus):
    """Converte graus (0-360) em ponto cardinal (8 direções)."""
    if pd.isna(graus):
        return None
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
    return "Noroeste"


def executar(ano: int):
    cfg.DIR_GOLD.mkdir(parents=True, exist_ok=True)
    origem = cfg.DIR_SILVER / cfg.nome_arquivo(ano, "silver")
    df = pd.read_csv(origem, parse_dates=["Data"])
    df["Direcao_cardinal"] = df["Direcao_vento"].apply(classificar_direcao)
    df["Ano"] = df["Data"].dt.year
    df["Mes"] = df["Data"].dt.month
    destino = cfg.DIR_GOLD / cfg.nome_arquivo(ano, "gold")
    df.to_csv(destino, index=False)
    log.info("[gold] %s: %d linhas -> %s", ano, len(df), destino)
    return destino
