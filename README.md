# Pipeline El Niño – São Paulo

Arquitetura medalhão (bronze → silver → gold), **um ano e um período por execução**.

| Etapa | Módulo | Saída |
|---|---|---|
| bronze | `pipeline/bronze.py` (API Open-Meteo) | `arquivos/bronze/sp_ANO_MMDD_MMDD_bronze.csv` |
| silver | `pipeline/silver.py` (limpeza/tipagem/colunas em PT) | `arquivos/silver/sp_ANO_MMDD_MMDD_silver.csv` |
| gold | `pipeline/gold.py` (direção cardinal, Ano, Mes) | `arquivos/gold/sp_ANO_MMDD_MMDD_gold.csv` |

## Uso
```bash
pip install -r requirements.txt
python run_pipeline.py 1982                                        # período padrão (01-06 a 31-08)
python run_pipeline.py 1982 --data-inicial 03-15 --data-final 09-10  # de 15/03 a 10/09
python run_pipeline.py 1990 --data-inicial 11-01 --data-final 12-31  # outro ano, outro período
```
Datas no formato `MM-DD`. O período padrão fica em `config/config.py`.
O nome do arquivo inclui o período, então períodos diferentes do mesmo ano não se sobrescrevem.
O CSV final para uso é o da pasta `gold`.

Observação: `precipitation_probability_max` foi removida, pois só existe na API de previsão, não na histórica.
