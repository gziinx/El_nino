"""Pipeline El Niño (São Paulo): bronze -> silver -> gold, para UM ano por vez.

Uso:
    python run_pipeline.py 1982
    python run_pipeline.py 1982 --data-inicial 03-15 --data-final 09-10
    python run_pipeline.py 1982 --data-inicial 11-01 --data-final 12-31

Saída (o CSV final, pronto para uso, é o da gold):
    arquivos/bronze/sp_1982_0315_0910_bronze.csv
    arquivos/silver/sp_1982_0315_0910_silver.csv
    arquivos/gold/sp_1982_0315_0910_gold.csv
"""
import argparse
import logging
import re
import sys
import time
from datetime import date, datetime

from config import config as cfg
from pipeline import bronze, gold, silver

ETAPAS = [("bronze", bronze.executar), ("silver", silver.executar), ("gold", gold.executar)]
PADRAO_MMDD = re.compile(r"^(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Pipeline El Niño (São Paulo) - um ano por execução")
    ap.add_argument("ano", type=int, help="ano desejado, ex.: 1982")
    ap.add_argument("--data-inicial", metavar="MM-DD", help=f"padrão: {cfg.DATA_INICIAL}")
    ap.add_argument("--data-final", metavar="MM-DD", help=f"padrão: {cfg.DATA_FINAL}")
    args = ap.parse_args(argv)

    if not cfg.ANO_MINIMO <= args.ano <= date.today().year:
        ap.error(f"ano deve estar entre {cfg.ANO_MINIMO} e {date.today().year}")
    for valor in (args.data_inicial, args.data_final):
        if valor and not PADRAO_MMDD.match(valor):
            ap.error(f"data '{valor}' inválida, use o formato MM-DD (ex.: 06-01)")
    if args.data_inicial:
        cfg.DATA_INICIAL = args.data_inicial
    if args.data_final:
        cfg.DATA_FINAL = args.data_final

    # Datas reais (barra 02-30, ou 02-29 em ano não bissexto) e em ordem
    try:
        ini = datetime.strptime(f"{args.ano}-{cfg.DATA_INICIAL}", "%Y-%m-%d")
        fim = datetime.strptime(f"{args.ano}-{cfg.DATA_FINAL}", "%Y-%m-%d")
    except ValueError:
        ap.error(f"data inexistente em {args.ano}: {cfg.DATA_INICIAL} ou {cfg.DATA_FINAL}")
    if ini > fim:
        ap.error("a data inicial deve ser anterior (ou igual) à data final")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%H:%M:%S")
    log = logging.getLogger("pipeline")
    log.info("Ano %s | período %s até %s", args.ano, cfg.DATA_INICIAL, cfg.DATA_FINAL)

    for nome, executar in ETAPAS:
        t0 = time.time()
        try:
            executar(args.ano)
        except Exception:
            log.exception("Falha na etapa '%s'. Pipeline interrompido.", nome)
            return 1
        log.info("Etapa '%s' concluída em %.1fs", nome, time.time() - t0)

    log.info("Pronto! CSV final: %s", cfg.DIR_GOLD / cfg.nome_arquivo(args.ano, "gold"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
