"""SILVER: limpeza, tipagem e tradução das colunas -> arquivos/silver/."""
import logging

import pandas as pd

from config import config as cfg

log = logging.getLogger(__name__)


def transformar(df: pd.DataFrame, ano: int) -> pd.DataFrame:
    df = df.copy()

    # Duplicados
    duplicados = int(df.duplicated().sum())
    if duplicados:
        log.warning("[silver] %s: %d linhas duplicadas removidas", ano, duplicados)
        df = df.drop_duplicates()

    # Tipos
    df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%d", errors="raise")
    colunas_num = [c for c in df.columns if c != "time"]
    df[colunas_num] = df[colunas_num].apply(pd.to_numeric, errors="coerce")

    # Nulos (só avisa; não inventa valores)
    nulos = df.isnull().sum()
    if nulos.sum():
        log.warning("[silver] %s: valores nulos por coluna:\n%s", ano, nulos[nulos > 0])

    df = df.sort_values("time").reset_index(drop=True)
    return df.rename(columns=cfg.COLUNAS_PT)


def executar(ano: int):
    cfg.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    origem = cfg.DIR_BRONZE / cfg.nome_arquivo(ano, "bronze")
    df = transformar(pd.read_csv(origem), ano)
    destino = cfg.DIR_SILVER / cfg.nome_arquivo(ano, "silver")
    df.to_csv(destino, index=False)
    log.info("[silver] %s: %d linhas -> %s", ano, len(df), destino)
    return destino
