import pandas as pd


t_sp_25_ddm = pd.read_csv('arquivos/tgt/t_sp_25_tgt.csv')
t_sp_26_ddm = pd.read_csv('arquivos/tgt/t_sp_26_tgt.csv')

print(t_sp_26_ddm.info())

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
t_sp_25_ddm["direcao_cardinal"] = t_sp_25_ddm[
    "Direcao_vento"
].apply(classificar_direcao)

t_sp_26_ddm["direcao_cardinal"] = t_sp_26_ddm[
    "Direcao_vento"
].apply(classificar_direcao)

print(t_sp_25_ddm.tail())